# Introduction #
## See AusDemo (4 mins) ## 

Google Drive Viewing:

https://drive.google.com/file/d/16oW1dRiq_u4ZN3qxBIXiMuIVZA94ImE8/view?usp=sharing


Google Drive Downloading:

https://gdurl.com/cIDc/download

P.S. You can also download other demo for history versions or more details in Others/OtherDemo
## Also, See "User Manual.pdf" in folder "Others" ## 
### for a quickly understand of ### 
### how this system working ###
### and basic operating principles and processes ###


# !!!ATTENTION!!! #

## Manual Run Instructions ##

1. Navigate to the "Group14JFC" directory.
2. Run the following commands:

Terminal 1
```
cd aus\ausback
python manage.py runserver
```
Terminal 2
```
cd ..\aus\ausfront
npm install
npm run dev
```
Terminal 3
```
cd ..\Hardware
node app.js
```
3. Wait for the servers to start up and confirm by checking the console outputs.

4. Once all servers are running, open your web browser and go to 
                      http://localhost:5173/ 
5. You are ready to go ~

## Quick Run for Windows ##

Click on the "AusStart"

Wait for the website to show up

## Quick Run for MacOS ##

* May not work for now and better use the manual start up

Click on the "AusStart - MacOS"

Wait for the website to show up


# Good Luck & Have Fun! #
## --------------------Software Readme starts here----------------------- ##
# AMOD || Auscultation Model of Dog #
## This is the application for the JFC Group 14 - Dog Auscaltation Model. ##
### Start from 1st Dec, 2023 ###
### Expect to finish at 9th Feb, 2024 ###
## The objectives are: ##
    A user interface
    Process signal that comes from the hardware part
    Store the simulation sound sent to the model
    Send properly the audio to the model through the BLE
    Help the student to identify a abnormal sound
    Train the student to count the heatbeat
Updated 20231201

# Initialization #
## Frontend ##
  You need python for the following int
  pip install node (download the node.js from the web is more recommended)
  pip install npm (best using the admin mode)
  npm install (update the packages inside of ausfront folder)
  then 
  npm run dev
## Backend ##
  python manage.py migrate
  python manage.py initialDb
  python manage.py runserver


# Frontend - vue3 + Vite #
## Creating: ##
```
PS D:\Group14JFC\aus> npm create vue@latest
Need to install the following packages:
create-vue@3.8.0
Ok to proceed? (y) y

Vue.js - The Progressive JavaScript Framework

√ Project name: ... ausfront
√ Add TypeScript? ... Yes
√ Add JSX Support? ... Yes
√ Add Vue Router for Single Page Application development? ... Yes
√ Add Pinia for state management? ... Yes
√ Add Vitest for Unit Testing? ... Yes
√ Add an End-to-End Testing Solution? » No
√ Add ESLint for code quality? ... Yes
√ Add Prettier for code formatting? ... Yes

Scaffolding project in D:\Group14JFC\aus\ausfront...
```
Done. Now run:
```
  cd ausfront
  npm install
  npm run format
  npm run dev
```
# Recommend Tools #

BootStrap
FontAwesome
Rest_framework

# Backend - Django #
django-admin startproject ausback
cd ausback
python manage.py startapp aus
+ management/commands
+ static/.csv
+ installed_apps...
  rest_frameworks and cors

# Key Words #
### Vue 3 ###
  Framework for frontend development
### Vite ###
  Build Tools for automatically application build
### Vuex ###
  Official status management library (store)
### ESLint ###
  Javascript code inspection and repair tool
### Prettier ###
  Code formatting tools
### Element plus ###
  Component library, providing rich UI components and styles
### Gdurl.com ###
  For creating link to view or download the files on Google Drive

# Development #
## Each time after ##
```
  git pull
```
### Frontend ###
Run
```
  npm install
  npm run dev
```
### Backend ###
Run for normal situations:
```
  python manage.py migrate

  python manage.py runserver
```
#### OR ####
Run when database updating needed:
```
  python manage.py deleteAll
  python manage.py migrate
  python manage.py initialDb

  python manage.py runserver
```

# Current Issues #
0. For mac, start up havent been set yet
1. creating refreshing problems:
   Can not keep the website interface(typical audio name in practice page and current list in teaching dashboard) 
   updating to all the things after each edit or remove actions
    Maybe caused by asyc issues?
2. Need to be able to automatically change to the new list we created
3. diff current list have different active sounds, make a choice for selecting diff list in practice page
4. Current list should not change after change page, eg. from teaching dashboard to practice page and change back
5. There should be a current list instruction on the practice page
6. How to handle very long list name?



# Solved Issues #

1. rename and remove too similar to each other --- delete list
2. help page still need imporve with icon
3. bigger icons for heart and lungs
4. switch the position of audio library and current list
5. use different color rather than orange
6. list saving (creating or updating)
7. Attention: no list content cleaning after remove the list
8. No list can have the same name
9. mounted of style in Help Page
10. sorting mechnithm for heartand lungs
11. searching bar will be good
12. CRUD for the audio content (interface design)
13. When cancel the add new list action, a default listX is still added
14. Audio edit dialog (backend database saving action)
15. Link will expire and local storage needed...
16. Time needed before active audio are ready to play (preloading? or Local database?)
17. After we have local storage, browse and import audio function is needed
18. can't edit the audio name in the edit mode
19. Add mode cant deal with file uploading
20. When adding new audio data, you need to provide all the information (excluding description)
21. sovled with optimized delete list content accordingly: Removing a audio from audio library may trigger some bug when I have added a lot of audio to one or more current lists
22. Could be, the id could not be the same when add-in new audio data
23. 'Active' should be changed to another word, also the icon
24. getActiveHeartAudio and getActiveLungAudio
25. 'Active' icon needs to be explained
26. deBug - there are multiple lists that has activated audio

# That's All for our Ausculation System ! 
## MANY MORE THANKS TO：

Jacoranda Flame Consulting (JFC)

USYD Vet School

And my Great Group 14 !!! 

Rahul, Ziyuan, James, Ying and Dhamo. 

We are Awesome !

## Author: ##
Renjie Yao 09/02/2024
