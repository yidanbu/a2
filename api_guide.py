import os
import uuid

from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename

from database import *
from utils import role_required

guide_api = Blueprint('guide_api', __name__)


@guide_api.route("/", methods=['GET'])
@role_required('apiarist', 'staff', 'admin')
def guide():
    # get all guides with primary image
    results = query("select * from guide, image where guide.id = image.guide_id and image.is_primary;")
    print(results)
    return render_template('guide.html', user=session, guide_list=results)


@guide_api.route("/upload", methods=['GET'])
@role_required('staff', 'admin')
def upload_guide_page():
    return render_template('upload_guide.html', user=session)


@guide_api.route("/<id>", methods=['GET'])
def guide_detail_page(id):
    result = query("select * from guide where id=%s;", (id,))
    if not result:
        return jsonify({"guide": None}), 404
    images = query("select * from image where guide_id=%s;", (id,))
    if not result:
        return jsonify({"guide": None}), 404
    return render_template('edit_guide.html', user=session, guide=result[0], images=images)


@guide_api.route("/<id>", methods=['DELETE'])
@role_required('staff', 'admin')
def delete_guide(id):
    query("DELETE FROM image WHERE guide_id=%s;", (id,))
    query("DELETE FROM guide WHERE id=%s;", (id,))
    return jsonify({}), 200


@guide_api.route("/", methods=['POST'])
@role_required('staff', 'admin')
def upload_guide():
    disease_info = {
        'type': request.form['type'],
        'exists_in_nz': True if request.form['exists_in_nz'] == 'yes' else False,
        'common_name': request.form['common_name'],
        'scientific_name': request.form['scientific_name'],
        'key_characteristics': request.form['key_characteristics'],
        'description': request.form['description'],
        'symptoms': request.form['symptoms']
    }
    print(request.form)  # 实际应用中应保存到数据库
    # 图片文件
    uploaded_files = request.files.getlist('images[]')
    print(uploaded_files)
    filenames = []
    for index, file in enumerate(uploaded_files):
        if file:  # 如果文件存在
            filename = str(uuid.uuid4()) + secure_filename(file.filename)
            filenames.append(filename)
            file.save(os.path.join(config.upload_folder, filename))

    # transactional database operation
    connection, cursor = get_connection_and_cursor()
    try:
        cursor.execute(
            "INSERT INTO guide (type, exists_in_nz, common_name, scientific_name, key_characteristics, description, symptoms) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (disease_info['type'], disease_info['exists_in_nz'], disease_info['common_name'], disease_info['scientific_name'], disease_info['key_characteristics'], disease_info['description'], disease_info['symptoms'])
        )
        guide_id = cursor.lastrowid
        image_data = [(guide_id, filename, True if index == int(request.form['primary_image']) else False) for index, filename in enumerate(filenames)]
        cursor.executemany(
            "INSERT INTO image (guide_id, filename, is_primary) VALUES (%s, %s, %s);", image_data
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("guide_api.guide"))


@guide_api.route("/<id>", methods=['PUT'])
@role_required('staff', 'admin')
def update_guide_basic_info(id):
    query("UPDATE guide SET type=%s, exists_in_nz=%s, common_name=%s, scientific_name=%s, key_characteristics=%s, description=%s, symptoms=%s WHERE id=%s;",
          (request.json['type'], request.json['exists_in_nz'], request.json['common_name'], request.json['scientific_name'], request.json['key_characteristics'], request.json['description'], request.json['symptoms'], id))
    return jsonify({}), 200


@guide_api.route("/<id>/image/<image_id>/primary", methods=['PUT'])
@role_required('staff', 'admin')
def guide_image_set_primary(id, image_id):
    # transactional database operation
    connection, cursor = get_connection_and_cursor()
    try:
        cursor.execute("UPDATE image SET is_primary = 0 WHERE guide_id = %s;", (id,))
        cursor.execute("UPDATE image SET is_primary = 1 WHERE id = %s;", (image_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify({}), 200


@guide_api.route("/<id>/image/<image_id>", methods=['DELETE'])
@role_required('staff', 'admin')
def guide_image_delete(id, image_id):
    result = query("select * from image where id=%s;", (image_id,))
    if not result:
        return jsonify({"error": "image not found"}), 404

    if result[0]['is_primary']:
        return jsonify({"error": "cannot delete primary image"}), 400
    query("DELETE FROM image WHERE id=%s;", (image_id,))
    return jsonify({}), 200


@guide_api.route("/<id>/image", methods=['POST'])
@role_required('staff', 'admin')
def guide_image_upload(id):
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        file.save(os.path.join(config.upload_folder, filename))
        query("INSERT INTO image (guide_id, filename, is_primary) VALUES (%s, %s, 0);", (id, filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file extension'}), 400
