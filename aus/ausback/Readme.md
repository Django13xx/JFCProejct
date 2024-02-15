# Basic Commands
## enable virtual
    .\.venv\Scripts\Activate
## Package installation
    pip install django
    pip install djangorestframework
    pip install django-cors-headers

# Backend developing History
2023/12/4
12:06 PM
+ Backend created
+ models initialized with a table Audio


2023/12/6
To do:
Database setup for user account
Functionality of login and register


2023/12/08
9:52 AM
+serializers.py created for
    Use Rest_framework for model export
+ static/.csv files
+ management/commands/initialDb
    For initializing the database
Run
``
    python manage.py initialDb
``
+ installed _app modified in settings.py
    to get access to rest_framework
= modified urls.py
    create views for backend/database models
+ admin.py has been added
    also use for superuser creating
``
    python manage.py createsuperuser
``
base_url/admin is accessible

+ aus/templates/home.html
    For home page creating in the backend
    quickly access database (guide page)

= Added the CORS settings inside of settings.py

2023/12/11
14:14
Note:
1. How to create new models:
In './ausback/aus/models.py': Modify required class
In same level of manage.py, open Terminal: '$ python manage.py makemigrations' to automatically create database migration
Then '$ python manage.py migrate' to apply migration

2. How to initialize database:
Under './ausback/static' create new csv file to store class's attributes
Then in '.ausback/aus/management/commands/initialDb.py': make new operation lines to read and write information from csv file to the database
In same level of manage.py, open Terminal: '$ python manage.py initialDb' to port initial data in csv to database

3. How to import static csv file into database:
'$ manage.py migrate'

22/01/2024
Added login function, modified models.py urls.py and settings.py

2023/12/14
11:41
Renjie Yao:
+ New commands file inside management/commands "deleteAll.py"
### For change the models structure in the backend ###
    1. run
        python manage.py deleteAll
    2. modify the models.py
        add new columns or ...remember to set default values
    3. update the changes
        python manage.py makemigrations
        python manage.py migrates
    4. update the .csv files and initialDb.py file according to the changes
    5. run
        python manage.py initialDb
    6. Check again everything is fine.

To do:
    need a new model: LIST
        store the data of each setup list (year 1, list 2 ...) contains different audio
    Conduct the getAllAudio function
        remember to pre handle the database to form a json response set

16:27
LIST established, data needed
Ready for BE & FE Connection

2023/12/15
10:48
= views.py, home.html, urls.py
    setup the getAllAudio function and corresponding API
    The JSON file creating process is suitable for most of the situations
    The frontend now can only access the api/getAllAudio under development mode
    *more info are included in the ausfront readme.md
11:05
To Ziyuan,
    Conduct a getAllList() and its API


10/01/2024
Add
    addNewAudio
For add new audio to audio library by our users


12/01/2024
Done:
    Can access audio files in media/audio directly from BE
Trying to:
    make the audio files accessable from FE
        details in frontend readme