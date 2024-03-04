import datetime
import os

from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import uuid

import config
from database import *
from utils import hash_password, role_required

guide_api = Blueprint('guide_api', __name__)


@guide_api.route("/", methods=['GET'])
def guide():
    # get all guides with primary image
    results = query("select * from guide, image where guide.id = image.guide_id and image.is_primary;")
    print(results)
    return render_template('guide.html', guide_list=results)


@guide_api.route("/upload", methods=['GET'])
@role_required('staff')
def upload_guide_page():
    return render_template('upload_guide.html')


@guide_api.route("/", methods=['POST'])
@role_required('staff')
def upload_guide():
    disease_info = {
        'type': request.form['type'],
        'exists_in_nz': bool(request.form['exists_in_nz']),
        'common_name': request.form['common_name'],
        'scientific_name': request.form['scientific_name'],
        'key_characteristics': request.form['key_characteristics'],
        'description': request.form['description'],
        'symptoms': request.form['symptoms']
    }
    print(request.form)  # 实际应用中应保存到数据库

    # 图片文件
    uploaded_files = request.files.getlist('images[]')
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
        image_data = [(guide_id, filename, True if index == request.form['primary_image'] else False) for index, filename in enumerate(filenames)]
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

    return jsonify({}), 200
