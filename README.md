**Companion App**

**Authors**: José Alvarado, Daniel Suazo and Diego Méndez


### Description of the application
The purpose of the Companion App is to facilitate the course selection process for students at the UPRRP. The concept is achieved by offering a variety of tools to the user:

1. Keeping a record of the courses that the student has already taken while they progress through their degree. 

2. The app uses the data entered by the student to compute the GPA, this allows the user to keep track of it and have it handy for all academic purposes. 

3. The student can login with his/her gmail account from the university, instead of login with SSN from a terminal.

4. It presents the list of classes that the university has made available for the upcoming semester. This allows the user to choose the courses that they look forward to enrolling in.

5. With the selected courses and their allocated times, the app provides the option to create an agenda with the selected courses in time-blocks organized in a weekly format.

The goal is to help students organize themselves, practice their enrollments and evaluate all of their options before using the university's system for the official process.

### Requirements:
- Python 3.4+
- Postgres
- PgAdmin (UI to see your database): https://www.pgadmin.org/
- Ngrok free version: https://ngrok.com/
- Postman (test endpoints): https://www.postman.com/
- npm and node: https://www.npmjs.com/get-npm
- Expo ios or android mobile app to run application in physical device
- Android studio to run application in emulator

### SPECIAL NOTES BEFORE STARTING:
- While following the steps below, if you get the following messages in your terminal:
    - **Superuser creation skipped due to not running in a TTY. You can run manage.py createsuperuser in your project to create one manually**
    - **Watching for file changes with StatReloader**
- Just add the word winpty at the beginning of each command. Examples:
    - **winpty python manage.py createsuperuser**
    - **winpty python manage.py runserver**


# Below are the steps to run the application

### Step 1: Run in your terminal
- git clone https://github.com/dmr1725/CompanionApp.git


### Step 2: Go to the server directory and run in your terminal
- In you already have django, create a virtual environment and run **pip install -r requirements.txt**. 
- If not, then just run **pip install -r requirements.txt** inside the server directory. 


### Step 3: Create database
- Create postgres database in PgAdmin called ‘**iupi**’
- Go to **server/restful/settings.py**
- Go to line 130 where it says ‘**DATABASES**’ and fill your data in ‘**USER**’ and ‘**PASSWORD**’ accordingly

### Step 4: change directories in files
- Go to **organizar/organizar.py** and change the paths in lines 4, 5 and 6 to your path
- Go to **server/CompanionApp/views.py** and change paths in lines 3, 64 and 111 to your path. **NOTE: in line 64 you need to change 2 paths**


### Step 5: make migrations of django project
- Go to the server directory and run:
    - **python manage.py makemigrations**
    - **python manage.py migrate**
- After running these 2 commands successfully, go to pgAdmin and go to the ‘**iupi**’ database. Then from the **iupi** database go to **Schemas/Tables**.You should see 22 tables.

### Step 6: create endpoints in postman
- Open postman and create a new collection called ‘**CompanionApp**’
- Inside the collection ‘**CompanionApp**’ we’re going to create 3 post requests
- To create a request inside a collection, just click the three dots (‘...’) of the collection ‘**CompanionApp**’ and then click ‘**Add Request**’. Enter the name of the request. Look for the request and change the ‘**GET**’ method to a ‘**POST**’ method and insert a url. 
    - First request call it ‘**Insert every faculty**’. Change it to a ‘**POST**’ request. Set url to ‘**http://127.0.0.1:8000/api/insertar_fac**’
    - Second request call it ‘**Insert courses**’. Change it to a ‘**POST**’ request. Set url to ‘**http://127.0.0.1:8000/api/insertar_cursos**’
    - Third request call it ‘**Insert courses for next semester**’. Change it to a ‘**POST**’ request. Set url to ‘**http://127.0.0.1:8000/api/insertar_prox_sem_cursos**’ 

### Step 7: insert faculties, unique courses and courses for next semester with the endpoints created in step 7
- Go to the **server** directory in the terminal and type ‘**python manage.py runserver**’
- Let the terminal run and go to Postman.
    - Click send in the endpoint called ‘**Insert every faculty**’ and wait for it to finish.
    - Then, click send in the endpoint called ‘**Insert courses**’ and wait for it to finish.
    - Finally, click send in the endpoint called ‘**Insert courses for next semester**’ and wait for it to finish.
- After running successfully these 3 endpoints, quit the server and go to PgAdmin and look for the database ‘**iupi**’. Go to tables “**CompanionApp_facultad**”, “**CompanionApp_curso**” and “**CompanionApp_proximosemestre**” and you should see these tables with values. 

### Step 8: create django superuser
- go to the server directory in the terminal and type ‘**python manage.py createsuperuser**’
    - For username: ‘admin’
    - For email address: ‘admin@admin.com’
    - For password: ‘admin’
- **You can type whatever you want in username, email and password. Just remember these credentials because we’re going to use them later on.** 
- Now you can go to the **server** directory and run ‘**python manage.py runserver**’. Then go to your browser and paste this url ‘**http://127.0.0.1:8000/admin**’. Login as admin and explore django admin. 


### Step 9: create site in django admin
- Go to **server** directory in the terminal and type ‘**python manage.py runserver**’
- Then, go this url ‘**http://127.0.0.1:8000/admin**’ and login as admin.
- Once logged in, click where it says **SITES** and then click on **ADD SITE**
    - Domain name: **localhost:8000**
    - Display name: **localhost:8000**
    - Click save


### Step 10: create a social application 
- You'll need to create a project inside **https://console.developers.google.com/**. If you don't have an account, create one. 
- Inside your developers console project, you'll need to create two OAuth client ID. One for **ios** and one for **android**
- Some helpful tutorials to create a project and create OAuth client ID's:
    - For creating ios and android client id: **https://medium.com/@inaguirre/react-native-login-with-google-quick-guide-fe351e464752** 
        - In this tutorial, just go to where it says **"Google Console Project Setup"** and create your client id's for both ios and android.
    - Overall guide to create project in google developers console: **https://www.youtube.com/watch?v=xH6hAW3EqLk&t=527s**
- After you have your client id's for both ios and android, go to **client/Screens/Login.js**:
    - In line 26, insert your **IOS_CLIENT_ID**
    - In line 28, insert your **ANDROID_CLIENT_ID**
- Now, go to **server** directory in the terminal and type ‘**python manage.py runserver**’
- Then, go this url ‘**http://127.0.0.1:8000/admin**’ and login as admin.
- Once logged in, go to the bottom of the page and click on ‘**Social applications**’ and then click on ‘**ADD SOCIAL APPLICATION**’
    - Provider: **Google**
    - Name: **Google Login**
    - Client id: **Your IOS_CLIENT_ID**
    - Sites: double click on **localhost:8000**  
    - Click save


### Step 11: find id of site localhost:8000
- Go to **server** directory in the terminal and type ‘**python manage.py shell**’
- Inside the shell, run these commands:
    - **from django.contrib.sites.models import Site**
    - **Site.objects.all()**
        - This will return a list of your sites [‘example.com’, ‘localhost:8000’]
        - Step 3 will be the tricky part
    - Run in your terminal: **Site.objects.get(id=1)**
        - If you get an error you will need to run the same command above, but adding one to id. You will continue to do this until you get a return value of **localhost:8000**. Example: **Site.objects.get(id=2)**, **Site.objects.get(id=3)**, **Site.objects.get(id=4)**... My guess is that your value will be where id is between 4 and 7
    - **Enter: ‘quit()’ in the shell**
- Once you get your site id, go to **server/restful/settings.py**
- In settings.py go to line 76 and change the value from **SITE_ID** to your value and save the file

### Step 12: start with the frontend
- Go to the **client** directory in the terminal and type **npm install** to install all the dependencies of the frontend application. It will ask you to install **expo-cli** and you will say yes. 

### Step 13: run ngrok
- Ngrok will act as our localhost and will allow us to connect the frontend with the backend
- In your computer, go to where you installed ngrok. Click ‘ngrok.exe’. Inside the terminal of ngrok, type the following: ngrok http 8000 
- This will return two urls in the forwarding columns. For example it will return something like the two urls below:
    - **http://cc10e7b7abf5.ngrok.io**
    - **https://cc10e7b7abf5.ngrok.io**
**The two urls above won’t function. They are just examples**
- Then, copy one of those urls, returned by ngrok (preferably the one with https)
- Then, you will paste that url in various files inside the directory **client/Screens**
- First let me give you an example
    - You’ll see urls like these in the files: **http://7f9219a069f7.ngrok.io/api/add_taken_course** 
    - In this case, you’ll need to replace **http://7f9219a069f7.ngrok.io** with the one above **http://cc10e7b7abf5.ngrok.io**
    - The end result should like this **http://cc10e7b7abf5.ngrok.io/api/add_taken_course** instead of this **http://7f9219a069f7.ngrok.io/api/add_taken_course**
- You’ll need to replace your ngrok url in the following files inside the directory **client/Screens**:
    - **AddTakenCourse.js**: lines 55 and 95
    - **Agenda.js**: line 33
    - **CurrentCourses.js**: line 57 and line 89
    - **EditGrades.js**: line 53, line 75 and line 120
    - **EnrollNextSemester.js**: line 58 and line 96
    - **HomeScreen.js**: line 15
    - **Login.js**: line 46 and line 67
    - **Logout.js**: line 13
    - **MyCurriculum.js**: line 23 and line 46
    - **UpdateSemYear.js**: line 24 and line 51
- **NOTE: EVERY TIME YOU WANT TO RESTART THE APP, YOU’LL NEED TO RESTART NGROK AND REPLACE THE NEW URL OF NGROK IN EACH FILE. THE REASON FOR THIS IS BECAUSE WE’RE USING THE FREE VERSION OF NGROK.**


### Step 14: run the app
- Open a terminal and go to the **client** directory and in your terminal and type ‘**npm start**’. After running successfully go to this url **http://localhost:19002**
- Open another terminal and go to the server directory and type ‘**python manage.py runserver**’
- Use your phone to scan the qr code from expo and use CompanionApp
- **It is mandatory that your phone uses the same wifi that your local computer is using**


# ADDITIONAL NOTES:
- For now, the agenda works only through the dates **dec 14 - dec 19**. The agenda works around 80%. When you enroll in courses and go to your agenda, you will get an error. Just **ctrl + s** the file **Agenda.js** and see your agenda through the dates **dec 14 - dec 19**. 
- **This issue will be solved in the future**

# How to use CompanionApp
- Everytime you complete an action on the screens **Add Taken Courses, Current Courses, Update Grades and Enroll Next Semester** wait for around 5 seconds to see a successful message
- Screens where you can refresh the content by scrolling down are: **Current Courses, Agenda and  Update Grades**
- On the screen **Add Taken Courses**: 
    - Type in the search box a course that you already have taken. When typing in the search box you need to enter the code of the course. After you find the course, enter the grade and the semester and year you took the course. Click submit. 
- On the screen **Agenda**: 
    - In order to see your agenda you’ll need to enroll for courses next semester. After you enroll in courses for next semester, refresh the page by scrolling down. You will see a loader pop up and refresh the page. 
- On the screen **Curren Courses**: 
    - In order to see your current courses, you’ll need to add courses that you have already taken or enroll in courses for next semester. After you complete those things, scroll down to refresh the page and see your current courses.
    - On this screen, you can click the course to see the information and you can also delete the course
- On the screen **Update Grades**: 
    - After you have registered for the app some courses, you will see a list of courses where you can filter by semester and year. Click on the course and update your grade or delete the course. On this screen you can also refresh the page by scrolling down.
- On the screen **Enroll Next Semester**:
    - Type in the search box for a course that you want to take for next semester. When typing in the search box, you need to enter the code of the course. You will get a list of courses. When you click on the course you want, you’ll see additional information about the course. If you want to enroll, click submit. 
- On the screen **My Curriculum**: 
    - This screen will show you a table of courses that you had taken by year and semester. You can filter those courses by year and semester. Also, you can see your GPA.
- On the screen **Set your semester and year**: 
    - you will report to the app what is your current semester and year. Pick the semester and year you are and it is mandatory that you click submit
