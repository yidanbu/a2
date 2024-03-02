# BRMM
Project Report: Web Application Structure and Design
Web Application Structure
Route	Function	Template
/	home	base.html
/listdrivers	listdrivers	driverlist.html
/listcourses	listcourses	courselist.html
/driverrundetails	driver_run_details	driverrundetails.html
/overallresults	overall_results	overallresults.html
/graph	showgraph	top5graph.html
/admin	admin_gateway	admin_base.html
/admin/junior_driver	junior_drivers	juniordriverlist.html
/admin/driver	driver_search	driversearch.html
/admin/edit_run_by_driver	edit_run_by_driver	editrunbydriver.html
/admin/edit_run_by_course	edit_run_by_course	editrunbycourse.html
/admin/add_driver	add_driver	adddriver.html
Data Flow
HTML pages use url_for to generate URLs based on function names.
Routes are defined with @app.route decorators and lead to corresponding functions.
Data is passed to templates using render_template and keyword arguments (kwargs).
Assumptions and Design Decisions
Assumptions
All user interactions occur through the front-end HTML, and no direct API calls are made.
Database entries are assumed to consist of valid data.
Design Decisions
Page Similarity:
Admin pages share the common ”admin_base.html“ template to maintain consistency and integrate admin-specific functionality.
Hidden Items:
The 'admin_gateway' link is selectively displayed on the 'base' page for exclusive access from the home page.
HTTP Methods:
POST is used for 'edit' and 'add' pages to align with RESTful conventions and prevent data duplication on page refresh.
Data Exchange:
Data processing is primarily handled in the backend to simplify data structures passed to front-end templates for ease of debugging.
Database Questions
SQL Statement to Create the 'car' Table:
CREATE TABLE IF NOT EXISTS car (
    car_num INT PRIMARY KEY NOT NULL,
    model VARCHAR(20) NOT NULL,
    drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'
);
Relationship Between the 'car' and 'driver' Tables:
FOREIGN KEY (car) REFERENCES car(car_num)
Inserting 'Mini' and 'GR Yaris' Details into the 'car' Table:
INSERT INTO car VALUES
    (11, 'Mini', 'FWD'),
    (17, 'GR Yaris', '4WD');
Setting Default Value:
To set a default value of 'RWD' for the 'driver_class' field, modify the field definition as follows:
-- Change
drive_class VARCHAR(3) NOT NULL
-- To
drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'
Importance of Different Routes for Drivers and Admin:
If logins were implemented, it is crucial for drivers and the club admin to access different routes for several important reasons:

Within the gateway, a 7-layer gateway can be used to control access permissions for different pages. For instance, distinct access control can be applied to routes starting with '/admin'. This is an effective method, often referred to as Access Control Lists (ACL) or permission control. It allows for precise control over which users or roles can access the admin pages.

It is possible to clearly differentiate administrator functionality from the URL. This is essential as a well-designed URL structure can provide a clear distinction between admin and regular user functions, enhancing security by reducing the risk of accidental or unauthorized access.

If all routes are open to the public, anyone can access the admin pages, potentially leading to privacy concerns and data leakage. This presents a significant privacy issue. Admin pages may contain sensitive information, such as personal data or financial records. Unauthorized access could result in data leakage.

There is a possibility of data tampering with edit/add functionalities if all routes are public. Indeed, if all routes are open, malicious users may attempt to manipulate data, such as altering scores or adding drivers without authorization. This could impact the fairness of competitions and data integrity.

This report provides an overview of the web application structure, highlights key design choices, and answers database-related questions while emphasizing the importance of access control for security and data integrity.

