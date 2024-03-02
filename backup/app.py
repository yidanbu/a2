import itertools as it
import sys
from datetime import datetime

import mysql.connector
from flask import Flask
from flask import render_template
from flask import request

import connect

app = Flask(__name__)

connection = None


def getCursor():
    global connection
    connection = mysql.connector.connect(user=connect.dbuser,
                                         password=connect.dbpass,
                                         host=connect.dbhost,
                                         port=connect.dbport,
                                         database=connect.dbname,
                                         autocommit=True)
    return connection.cursor()


def query(stmt, params=None):
    cursor = getCursor()
    cursor.execute(stmt, params)
    return cursor.fetchall()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/listdrivers")
def listdrivers():
    driver_list = query("select driver_id, first_name, surname, age from driver order by surname, first_name;")
    if app.debug: print(f"driver_list: {driver_list}")
    return render_template("driverlist.html", driver_list=driver_list)


@app.route("/listcourses")
def listcourses():
    course_list = query("SELECT * FROM course;")
    if app.debug: print(f"course_list: {course_list}")
    return render_template("courselist.html", course_list=course_list)


@app.route("/driverrundetails")
def driver_run_details():
    driver_list = query("SELECT * FROM driver;")
    # assemble option list to render html. format is [(driver id, driver name), (driver id, driver name), ...]
    option_list = [(d[0], f"{d[1]} {d[2]}") for d in driver_list]
    if app.debug: print(f"driver option list: {option_list}")

    driver = request.args.get("driver")
    if app.debug: print(f"querying driver detail for: {driver}")

    # if driver is None/empty, this is a simple page
    if not driver:
        return render_template("driverrundetails.html", drivers=option_list)

    # if driver has value, it is a query for driver detail
    driver_details = parse_driver_detail(query(
        "select driver_id, first_name, surname, model, drive_class, name as course_name, run_num, seconds, cones, wd "
        "from run r, driver d, course c, car "
        "where r.dr_id = d.driver_id and r.crs_id = c.course_id and d.car = car.car_num "
        f"and d.driver_id = {driver};"))
    return render_template("driverrundetails.html", drivers=option_list, driver_details=driver_details)


@app.route("/overallresults")
def overall_results():
    results = parse_overall_results(
        query("select driver_id, first_name, surname, age, model, crs_id, run_num, seconds, cones, wd "
              "from run r, driver d, car where r.dr_id = d.driver_id and d.car = car.car_num;"))
    return render_template("overallresults.html", overall_results=results)


@app.route("/graph")
def showgraph():
    # get top 5
    driver_overall_results = parse_overall_results(query(
        "select driver_id, first_name, surname, age, model, crs_id, run_num, seconds, cones, wd "
        "from run r, driver d, car where r.dr_id = d.driver_id and d.car = car.car_num;"))[:5]
    if app.debug: print(f"show graph driver overall results: {driver_overall_results}")
    # get best driver/results list from previous query
    # format: ["driver_id driver_name ",...]
    bestDriverList = [f"{result[0]} {result[1]} " for result in driver_overall_results]
    # format: [overall result for driver 1, overall result for driver 2,...]
    resultsList = [result[9] for result in driver_overall_results]

    # Insert code to get top 5 drivers overall, ordered by their final results.
    # Use that to construct 2 lists: bestDriverList containing the names, resultsList containing the final result values
    # Names should include their ID and a trailing space, eg '133 Oliver Ngatai '
    return render_template("top5graph.html", name_list=bestDriverList, value_list=resultsList)


# This function is admin gate way page route
@app.route("/admin")
def admin_gateway():
    return render_template("admin_base.html")


@app.route("/admin/junior_driver")
def junior_drivers():
    results = query("select d1.*, d2.first_name, d2.surname "
                    "from driver d1 join driver d2 on d1.caregiver = d2.driver_id order by d1.age desc, d1.surname;")
    # merge name
    # parse results to [[driver id, driver name, dob, age, car id, care giver name], ...]
    for index, result in enumerate(results):
        results[index] = [result[0], f"{result[1]} {result[2]}", result[3], result[4], result[5], result[6],
                          f"{result[7]} {result[8]}"]

    return render_template("juniordriverlist.html", drivers=results)


@app.route("/admin/driver")
def driver_search():
    param = request.args.get("query")
    # if query is empty, render initial page
    if not param:
        return render_template("driversearch.html")
    return render_template("driversearch.html",
                           drivers=query("select * from driver where first_name like %s or surname like %s",
                                         (f"%{param}%", f"%{param}%")))


@app.route("/admin/edit_run_by_driver", methods=["GET", "POST"])
def edit_run_by_driver():
    driver_list = query("SELECT * FROM driver;")
    driver_option_list = [(d[0], f"{d[1]} {d[2]}") for d in driver_list]
    # run option list format: [(A,1), (A,2),...]
    run_option_list = list(enumerate(it.product("ABCDEF", "12")))

    # if http method is get, return initial page
    if request.method == "GET":
        return render_template("editrunbydriver.html", drivers=driver_option_list, runs=run_option_list)

    # get query form params
    if app.debug: print(request.form)
    driver = request.form.get("driver")
    course_run = request.form.get("course_run")
    time: str = request.form.get("time")
    cone: str = request.form.get("cone")
    wd: str = request.form.get("wd")

    # validate fields
    # 1. time should be parsed to float
    if time:
        try:
            float(time)
        except ValueError:
            return render_template("editrunbydriver.html", drivers=driver_option_list, runs=run_option_list,
                                   message="invalid time format, time should be float")
    # 2. cone and wd should be parsed to int
    if cone and not cone.isdecimal():
        return render_template("editrunbydriver.html", drivers=driver_option_list, runs=run_option_list,
                               message="invalid cone format, cone should be int")

    if wd and not wd.isdecimal():
        return render_template("editrunbydriver.html", drivers=driver_option_list, runs=run_option_list,
                               message="invalid wd format, wd should be int")

    # 3. Nothing updated, time, cone, wd all empty
    if not any([time, cone, wd]):
        return render_template("editrunbydriver.html", drivers=driver_option_list, runs=run_option_list,
                               message="nothing updated!")

    # try update table
    course = run_option_list[int(course_run)][1][0]
    run = int(run_option_list[int(course_run)][1][1])
    dr_id = int(driver)

    # assemble update clauses
    clauses = []
    if time:
        clauses.append(f"seconds={time}")
    if cone:
        clauses.append(f"cones={cone}")
    if wd:
        clauses.append(f"wd={wd}")

    stmt = f"update run set {','.join(clauses)} where dr_id={dr_id} and crs_id='{course}' and run_num={run};"
    getCursor().execute(stmt)
    return render_template("editrunbydriver.html", drivers=driver_option_list, runs=run_option_list,
                           message="update success!")


@app.route("/admin/edit_run_by_course", methods=["GET", "POST"])
def edit_run_by_course():
    # course_option_list format: [(0,A), (1,B),...]
    course_option_list = list(enumerate("ABCDEF"))
    driver_list = query("SELECT * FROM driver;")
    driver_list = [(d[0], f"{d[1]} {d[2]}") for d in driver_list]
    # driver_run_option_list format: [(index, (driver id, driver name), run_id), ...]
    driver_run_option_list = list(enumerate(it.product(driver_list, "12")))

    # if http method is get, return initial page
    if request.method == "GET":
        return render_template("editrunbycourse.html", courses=course_option_list, driver_runs=driver_run_option_list)

    # get query params
    if app.debug: print(request.form)
    course = request.form.get("course")
    driver_run = request.form.get("driver_run")
    time: str = request.form.get("time")
    cone: str = request.form.get("cone")
    wd: str = request.form.get("wd")

    # validate fields
    # 1. time should be parsed to float
    if time:
        try:
            float(time)
        except ValueError:
            return render_template("editrunbycourse.html", courses=course_option_list,
                                   driver_runs=driver_run_option_list,
                                   message="invalid time format, time should be float")

    # 2. cone and wd should be parsed to int
    if cone and not cone.isdecimal():
        return render_template("editrunbycourse.html", courses=course_option_list,
                               driver_runs=driver_run_option_list,
                               message="invalid cone format, cone should be int")
    if wd and not wd.isdecimal():
        return render_template("editrunbycourse.html", courses=course_option_list,
                               driver_runs=driver_run_option_list,
                               message="invalid wd format, wd should be int")
    # 3. Nothing updated
    if not any([time, cone, wd]):
        return render_template("editrunbycourse.html", courses=course_option_list,
                               driver_runs=driver_run_option_list,
                               message="nothing updated!")

    # try update table
    course = course_option_list[int(course)][1]
    dr_id = int(driver_run_option_list[int(driver_run)][1][0][0])
    run = int(driver_run_option_list[int(driver_run)][1][1])
    # assemble update clauses
    clauses = []
    if time:
        clauses.append(f"seconds={time}")
    if cone:
        clauses.append(f"cones={cone}")
    if wd:
        clauses.append(f"wd={wd}")
    stmt = f"update run set {','.join(clauses)} where dr_id={dr_id} and crs_id='{course}' and run_num={run};"
    getCursor().execute(stmt)
    return render_template("editrunbycourse.html", courses=course_option_list,
                           driver_runs=driver_run_option_list,
                           message="update success!")


@app.route("/admin/add_driver", methods=["GET", "POST"])
def add_driver():
    car_list = query("SELECT * FROM car;")
    # format: [car id, car id, ...]
    car_option_list = [car[0] for car in car_list]

    # care-giver list should come from drivers
    drivers = query("SELECT * FROM driver;")
    care_giver_option_list = [(driver[0], f"{driver[1]} {driver[2]}") for driver in drivers]
    if request.method == "GET":
        return render_template("adddriver.html", cars=car_option_list, care_givers=care_giver_option_list)

    if app.debug: print(request.form)
    # validate fields
    if not request.form['fn']:
        return render_template("adddriver.html", cars=car_option_list, care_givers=care_giver_option_list,
                               message="first name cannot be empty")
    if not request.form['sn']:
        return render_template("adddriver.html", cars=car_option_list, care_givers=care_giver_option_list,
                               message="surname cannot be empty")

    if "is_junior" in request.form and request.form['is_junior'] == 'on' and not request.form['dob']:
        return render_template("adddriver.html", cars=car_option_list, care_givers=care_giver_option_list,
                               message="junior driver's date of birth cannot be empty")

    # get cursor here because auto incr id is needed to add to run
    cursor = getCursor()
    if "is_junior" in request.form and request.form['is_junior'] == 'on':
        cursor.execute("insert into driver (first_name, surname, date_of_birth, age, caregiver, car) "
                       "values (%s, %s, %s, %s, %s, %s)", (
                           request.form['fn'],
                           request.form['sn'],
                           request.form['dob'],
                           (datetime.now() - datetime.strptime(request.form['dob'], '%Y-%m-%d')).days // 365,
                           request.form['care_giver'],
                           request.form['car']
                       ))
    else:
        cursor.execute("insert into driver (first_name, surname, car) "
                       "values (%s, %s, %s)", (
                           request.form['fn'],
                           request.form['sn'],
                           request.form['car']
                       ))
    dr_id = cursor.lastrowid
    # add runs
    cursor.execute("insert into run (dr_id, crs_id, run_num) values "
                   f"({dr_id}, 'A', 1),"
                   f"({dr_id}, 'A', 2),"
                   f"({dr_id}, 'B', 1),"
                   f"({dr_id}, 'B', 2),"
                   f"({dr_id}, 'C', 1),"
                   f"({dr_id}, 'C', 2),"
                   f"({dr_id}, 'D', 1),"
                   f"({dr_id}, 'D', 2),"
                   f"({dr_id}, 'E', 1),"
                   f"({dr_id}, 'E', 2),"
                   f"({dr_id}, 'F', 1),"
                   f"({dr_id}, 'F', 2);"
                   )
    return render_template("adddriver.html", cars=car_option_list, care_givers=care_giver_option_list,
                           message="Add driver success!")


def parse_driver_detail(driver_details):
    # parse None field
    driver_details = [list(map(lambda x: 0 if None == x else x, driver_detail)) for driver_detail in driver_details]
    # calculate run total
    driver_details = [[*driver_detail, driver_detail[7] + 5 * driver_detail[8] + 10 * driver_detail[9]] for
                      driver_detail in driver_details]
    print(driver_details)
    for driver_detail in driver_details:
        # in this case, it means driver not run this time
        if driver_detail[7] == 0:
            driver_detail[7], driver_detail[8], driver_detail[9], driver_detail[10] = [""] * 4
    return driver_details


def parse_overall_results(overall_results):
    results = {}
    # add run total
    for index, overall_result in enumerate(overall_results):
        new_result = [*overall_result]
        if new_result[7] == None:
            new_result.append(None)
        else:
            new_result.append(overall_result[7] +
                              (5 * overall_result[8] if overall_result[8] else 0) +
                              (10 * overall_result[9] if overall_result[9] else 0))
        overall_results[index] = new_result

    # parse course time
    for overall_result in overall_results:
        # new driver
        if overall_result[0] not in results:
            # initialize result
            results[overall_result[0]] = {
                "name": f"{overall_result[1]} {overall_result[2]}{' (J)' if overall_result[3] and overall_result[3] <= 16 else ''}",
                "model": overall_result[4],
                "course_records": {"A": None, "B": None, "C": None, "D": None, "E": None, "F": None},
                "overall_result": None
            }
            # record run total
            # has run record
            if overall_result[10]:
                results[overall_result[0]]["course_records"][overall_result[5]] = overall_result[10]
        else:
            current_record = results[overall_result[0]]["course_records"][overall_result[5]]
            new_record = overall_result[10]
            if current_record == None or (
                    current_record != None and new_record != None and new_record < current_record):
                results[overall_result[0]]["course_records"][overall_result[5]] = new_record

    # get overall result
    for driver_id in results:
        course_records = results[driver_id]["course_records"]
        if None in course_records.values():
            results[driver_id]["overall_result"] = "NQ"
        else:
            results[driver_id]["overall_result"] = sum(course_records.values())

    # set result to list
    results = [
        [driver_id, result["name"], result["model"], result["course_records"]["A"], result["course_records"]["B"],
         result["course_records"]["C"], result["course_records"]["D"], result["course_records"]["E"],
         result["course_records"]["F"], result["overall_result"], ""] for driver_id, result in results.items()]

    # sort results by overall result
    results.sort(key=lambda x: x[9] if x[9] != 'NQ' else sys.float_info.max)

    # append rewards
    for index, result in enumerate(results):
        # cup
        if index < 1:
            result[-1] = "cup"
        elif 1 <= index < 5:
            result[-1] = "prize"
        else:
            break
    return results


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8001, debug=False)
    app.run(host="0.0.0.0", port=8001, debug=True)
