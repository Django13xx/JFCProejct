# Frontend developing History
2023/12/4
12:08 PM
+ Frontend created and can be opened by
    npm run dev

2023/12/6
+ all the views including Help, Login, MainPage and Register
+ Connect them together with index.ts
- delete all the unnecessary examples and templates
= modified App.vue for main layout
User are now able to change between start (login), practice (main page) and Help (example information)
User can register if they do not have a account
User can change to different mode and also here only from heart and lungs when doing practice
wireframe (For now): 
App
    -Practice (Anonymous)
    -Start
        -Register
        -Practice (using your account)
    -Help
Issues:
    Some bugs maybe tracked when routing after mode changing under the Practice page
To do:
    Writing about Functional Requirements
    Adjust the pages according to our requirements
    Backend initialization (See backend README for details)



2023/12/7
10：25
= Solve the problems of duplicated guide bar
wireframe (For now): 
Login
    -Practice (Anonymous)
    -Start(Login)
        -Register
        -Practice (using your account)
    -Help
To do:
    Finish the design of the register part
    Write Functional Requirements

10:30
+ Solve the switching problem of register 
    and now can switch between school register and personal register
To do:
    Write Functional Requirements

12:28
+ Connect the frontend and the backend
    the frontend can get access to the backend now

2023/12/11
09:52
Hi, Rahul ...............................................................................................................................................................
Please see the following commands from ChatGPT and solve the audio playing problem:
The audio_link seems to be a Google Drive link. However, keep in mind that direct linking to Google Drive files may not work for audio elements due to Google Drive's security settings.

To resolve this, you can modify the sharing settings of the audio file in Google Drive. Make sure that the file is accessible to anyone with the link, and try replacing the original Google Drive link with a direct link to the audio file. The direct link can be obtained by right-clicking on the file in Google Drive, selecting "Get link," and changing the sharing settings to "Anyone with the link can view."

Additionally, if the issue persists, consider hosting the audio files on a server that supports direct audio file streaming and update your API to provide links to these hosted files. This way, you can ensure compatibility with the <audio> element in your Vue.js application.

Do check if the audio play properly and can stay in a loop (will start again if finished)

Thanks! :)


2023/12/11
15:11
In './ausfront/index.html', change the website's name into "VetSci Aus APP"
Add our quit logo written by [Xi'Jie] (Coloured by Ziyuan)



2023/12/11
= src
working on the register and data transmit


2023/12/14
10:21
+ TeachingDashboardView.vue
    current play list
        apply to play the audio
        remove to delete the audio from the list
    audio library
        add to list to add this audio to the current list
    A list selector
        can add new list/ rename current list/ remove current list (cannot remove the last list)
Need to do:
    Play mode (current list can only for apply and no action for adding new songs from the library to the list)
    Edit mode (
        List and library: can remove audio in current list and can add new audio to the list from audio library
        List selector: can rename/remove/add new     list
    )
    Move the data to the backend and use API for connections
    achieve audio loop playing when "Apply" the audio
    The add to list movement will push the library table downwards which caused inconvenient
        Could remove the audio from the library and add it to the list
        Or, make them separate into left and right part

13:11
= HelpView.vue change the content to adapt to the new edition of our teaching page.
    Teaching Mode
    Auscultation Practice

15:20
    +Optimzied the formatting of guide bar as also the teaching view page

2023/12/15
= TeachingView, vite.config.ts
    Achieved the connection of getAllAudio under development mode
        CORS pros may rise up in the following deploying stage
        *see ausback readme.md for more information (same date)

12:29
+ success and warning dialog from element-plus added


15:57
= Help page
    Style optimized according to the User testing and suggestions in group discussion


18/12/2023
15:04
+ conduct audio list Add with axios.POST
+ conduct audio list Delete with axios.DELETE
Trying to conduct audio list update with axios.PUT


19/12/2023
12:39
+ use the viewset and serializers from rest framework can easily deal with CRUD
    successfully finished the CRUD of list, list content
To do:
Searching bar and sorting function

wait
    Delete of list content needed
    Working on it......
Start testing from
14:22


+ a dialog for adding all the new audios

still issues:
    no sorting functions
    no searching functions
    no true adding functions
    no list content cleaning after remove the list
next step, adding functions for audio library

21/12/2023
+ sorting function
+ rename function [implied with axios.delete()] * Why and How？
+ remove function for list content delete when list have been deleted

To do:
    Add and Edit audio in audio library


08/01/2024
+ Searching function with different fields
Working on:
    using gdurl.com to view audio file

16:04 pm

+ Finished the gdurl.com creating and database updating

To do:
    make the active heart/lung audio urls work
    try to play them in the MainPageView.vue

Solved the open pros of active Heart/Lung sound
    Hyper link serializer is trickyy

Working on:
    Play the Heart/Lung sound in the mainPageView.vue

Playable Heart/Lung audio which preset to active
Mix mode are now "play random heart beat"
To do:
Transmit the signal from TeachingView to MainView for
    setting the active heart/lung audio according to
    user's selection

10/01/2024
To do:
    user selected audio play in MainView from TeachingView
    Adding function for audio library
    Edit function for audio library
Done:
    Sorting function of audio library (Jay and Rahul)


11/01/2024
Finished:
    Remove the audio in the audio library (FE)
    Edit the audio in the audio library (FE)
    Function for different options in Main View
Debug:
    closing modal error
    change between different options in mainView
Working on:
    Edit audio content function
        frontend finished, but need function for backend updating...
To do:
    Create and save a New audio (FE)
    And their corresponding BE updating


15:56pm
Done:
    In MainPageView:
    Finished the basic about audio playing history (inculding cleaning function)
Optimized:
    Reverse the history to make the most recently appears in the top
Working on:
    save edit results to BE (Jay)

    Add new audio (Ziyuan)

    Help page updating (Rahul)

12/01/2024：
Done：
    Adding tooltip for buttons in Main View Page for improving user-friendly
To do:
    Save edit audio and info to BE
    Make audio title changeable in teachingDashboard
    Help page updating (Rahul)
    add new audio (Ziyuan)
Issues:
    Google Cloud Storage or CDN is not free and therefore, using backend storage first.
        Now try to access the media/audio/001.wav as an example
Done!

11:46 AM
    User testing needed and try to fullfilled the database
    The edit and add function for the audio library need new design for the new backend database

12:58 PM
    Debug the duple and wrong type errors in Main View

13:29 PM
    Functions for changing and deleting audio library data have been implemented

13:37 PM
    Functions for adding audio library data have been implemented

------ CRUD for audio library all done!!!

To do:
    adding audio part need file uploading functions
    Issues mention in the main README.md

15/01/2024
Done:
    File uploading functions
    Change the searching and primary key of list content to ID (from name)
Working on:
    Debugging for what I have done
To do:
    file uploading functions need debugging
    Issues mention in the main README.md

13:01
    change getAll() and corresponding functions for really reset (clear audioLibrary before each refreshing)
    change grade into upcase [Primary, Intermidiate, Advance]

To do:
    Adding function debugging and testing
    audio name is also changeable, check if everything is all right

Done:
    Resolved the problems of audio files deduction
Working on:
    CRUD debugging of both audio library and current list

    Debugging CRUD of current list

To do:
    When add new audio, we need a Elmessage for success notification (Done)
    And we need to be able to automaticlly change to the new list we created

Done：
    User testing
To do:
    Working on the getActiveHeartAudio & getActiveLungAudio for practise page getting active audios updated
    ...



22/01/2024
Working on Demo recording...
Done:
    Debug for active lung in different list can not be the same problem

02/02/2024
Done:
    Hardware connection
To do:
    The heartbeat mode (as teacher could clicked) have some issues needed to be fixed

05022024
To do:
    Change the playing mode's function into active heart/lungs random (and add new button to reactive the )

09/02/2024
Note of the element plus
// <template>
//   <el-button :plain="true" @click="open2">success</el-button>
//   <el-button :plain="true" @click="open3">warning</el-button>
//   <el-button :plain="true" @click="open1">message</el-button>
//   <el-button :plain="true" @click="open4">error</el-button>
// </template>

// <script lang="ts" setup>
// import { ElMessage } from 'element-plus'

// const open1 = () => {
//   ElMessage('this is a message.')
// }
// const open2 = () => {
//   ElMessage({
//     message: 'Congrats, this is a success message.',
//     type: 'success',
//   })
// }
// const open3 = () => {
//   ElMessage({
//     message: 'Warning, this is a warning message.',
//     type: 'warning',
//   })
// }
// const open4 = () => {
//   ElMessage.error('Oops, this is a error message.')
// }
// </script>








### The following are auto generated
------------------------------------------------------------------------------------------------
# ausfront

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1) Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2) Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
