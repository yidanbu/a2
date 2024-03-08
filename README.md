# TODO Items

- [x] Create an attractive home page which reflects a bee theme and has links to login and registration.
- [x] Create a login function with a single form where all users can enter a username and password (hidden).
- [x] Implement a password hashing and salting techniques to ensure secure storage of user passwords.
- [x] Provide a new user registration functionality that allows new Apiarists users to register and create an account
  themselves. In this process they will provide their details and set a unique username and password (at least 8
  characters long and have a mix of character types)
- [x] Define three user roles: Apiarists, Staff and Administrator.
- [ ] Implement a role-base access control system that restricts access to certain pages or features based on the user’s
  role.
- [x] Apiarists users should be able to manage their own profile (update personal information and change password).
- [x] Apiarists need to view the guide which will contain a primary image of each bee pest/disease, its common name, and
  whether it is currently present in NZ or not. Clicking on each primary image will reveal further detailed information
  such as scientific name, key characteristics, biology/description, symptoms and further images.
- [ ] Staff should be able to manage their own profile (update personal information and change password), view Apiarists
  profiles and manage the guide (view, add, update and delete details and images – including selecting the primary
  image).
- [ ] Administrators should have full access to the system and the ability to manage their own profile (update personal
  information and change password), manage Apiarists (view, add, update and delete), manage staff (view, add, update and
  delete) and manage the guide (view, add, update and delete details and images).
- [ ] Apiarists profile: first name, last name, apiarist id number, address, email, phone number, date joined, status (
  e.g., active, or inactive).
- [ ] Staff/Admin profile: staff number, first name, last name, email, work phone number, hire date, position,
  department, status.
- [ ] Bee Pest and Disease Guide (bee id, bee item type (e.g. pest or disease), present in NZ (yes or no), common name,
  scientific name, key characteristics, biology/description, symptoms, and images (including which image is the primary
  image).
- [ ] Content can be sourced from the websites below as well as your own research:
    - https://www.mpi.govt.nz/biosecurity/how-to-find-report-and-prevent-pests-anddiseases/bee-biosecurity/
    - https://www.mpi.govt.nz/dmsdocument/36975-New-Zealand-Bee-Biosecurity-VisualID-Guide
    - https://www.mpi.govt.nz/dmsdocument/58072-Bee-Biosecurity-The-EssentialsBooklet
- [ ] The database should contain at least 5 apiarists, 3 staff, one administrator, 10 bee pests/diseases present in NZ
  and 10 bee pests/diseases not present in NZ.
- [ ] Include a sources page within your webapp with references of your content material.
- [x] Design and implement a database schema and populate it with data to meet these requirements. In your design ensure
  you have considered data security, especially for usernames, passwords and biosecurity data.
- [ ] Create separate dashboard pages for each user role.
- [ ] Design and implement a visually appealing user interface for each dashboard that reflects the bee theme.
- [ ] Customise the functionality and features available on each dashboard based on the associated user role.
- [ ] A fully functional Flask Python web application for a bee pest and disease biosecurity guide that has a bee theme,
  with a login system and a role-based dashboards. 