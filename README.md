# DEV LINKS
#### Video Demo:  <URL HERE>
#### Description:
When applying for jobs or sharing your profile you may also want to include all you professional social media
links with your profile as well. For example GitHub, LinkedIN etc. Rather than remembering and copying it again
and again you can use devlinks to organise your links in an easy, efficient and professional manner.

#### Project Files:
**The main project files are app.py and helpers.py for the backend code.**
**The database used in sql and is named links.db.**
**The main project file for frontend is layout.html and all other html files extend from it to form different pages**

### Backend
#### helpers.py
helpers.py use most of the code from problem set 9. Includes two functions.
**login_required** function is used to ensure that a user is logged in before acessing website links
**apology** function is used to render an apology message on the screen if something goes wrong or the user enters incorrect input.

#### appy.py
This is the main file in the backend part of the project and is the heart of the entire web app. It includes all
the routes the user will use to access different portions of the website including the login and register route.
the **login_required** function is used before all the routes that the user can access only after login
Two important variables are defined at the top:
-**UPLOAD_FOLDER** : This defines the path where images uploaded by the user will be stored.
-**db** : This configures the CS50 library to use SQLite database.

A **brief overview** of each of the routes.
1. **/ route**: This is the main page and meet of the project. This route takes you to the link page where user can
                enter new links, modify existing links or delete existing links. The save button is used to update
                the SQLite database.
2. **/profile route**: This route takes you to the profile form where you can enter your other basic information and add
                       a picture as well.
3. **/preview route**: This is the final preview of the all you entered information and links which will be shared online.

#### links.db
This is the database used to share user information. It has 3 tables:
-**users**: Includes the username and password of a user in hashed. Has a unique id column that is used by other
            tables as Foriegn key.
-**links_data**: Contains the links information. Columsn include user_id that references the id column in userstable,
                 website column to show website name, and url column.
-**user_profiles**: Contains the profile information. Columns include first_name, last_name and email.

#### templates folder
This folder includes all the html files that app.py renders for different routes requested by the user. It also has the
layout.html file which is the base of all html files. It has the navbar and the main component inside which rest of the
templates are rendered.

## static folder
This folder includes the icons and images used by the web app in the images folder. Not all icons in the folder are used as there is still room for stylistic improvement in the project.
The uploads folder includes the images uploaded by the users.
Altough the project mainly uses bootstrap however there is a styles.css file that used some custom css styles.
