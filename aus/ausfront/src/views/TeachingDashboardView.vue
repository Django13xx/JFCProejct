<template>
  <div class="audio-player">
    <div class="controls">
      <div class="lists">
        <!-- This is the current list on the left side -->
        <div class="current-list">
          <h3 class="list-title">Current List</h3>
          <div class="current-list-table">
            <h3 class="list-title">
              <button @click="navigateLists('prev')" class="black-button">
                <i class="fas fa-chevron-left"></i>
              </button>
              <span>
                <select
                  id="listSelector"
                  class="listSelector"
                  v-model="selectedListId"
                  @change="loadSelectedList"
                >
                  <option v-for="list in availableLists" :key="list.id" :value="list.id">
                    {{ list.name }}
                  </option>
                </select>
              </span>
              <button @click="navigateLists('next')" class="black-button">
                <i class="fas fa-chevron-right"></i>
              </button>
            </h3>
            <div class="button-container">
              <button @click="addNewList" class="orange-button">
                <i class="fas fa-plus-circle fa-lg"></i> Create new List
              </button>

              <button @click="renameList" class="orange-button">
                <i class="fas fa-pencil-alt fa-lg"></i> Rename List
              </button>

              <button @click="removeList" class="orange-button">
                <i class="fas fa-trash-alt fa-lg"></i> Delete List
              </button>
            </div>
          </div>
          <div class="library-table">
            <table>
              <thead>
                <tr>
                  <th class="title th-clickable" @click="sortTable('title')">Title</th>
                  <th class="type th-clickable" @click="sortTable('type')">Type</th>
                  <th class="description th-clickable" @click="sortTable('description')">Description</th>
                  <th class="grade th-clickable" @click="sortTable('grade')">Grade</th>
                  <th class="Upload">Upload</th>
                  <th class="remove">Remove</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="song in currentList" :key="song.id">
                  <td>{{ song.title }}</td>
                  <td>
                    <i :class="getIconClass(song.type)"></i>
                  </td>
                  <td>{{ song.description }}</td>
                  <td>{{ song.grade }}</td>
                  <td>
                    <button
                      @click="apply(song)"
                      :class="{'applied': song.applied, 'orange-button': !song.applied}"
                    >
                      <i class="fas fa-upload" style="font-size: 1.5em;"></i>
                    </button>
                  </td>
                  <td>
                    <button @click="remove(song)" class="black-button">
                      <i class="fas fa-arrow-right" style="font-size: 1.5em;"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="space-between"></div> <!-- Add a container for space between -->
        <!-- This is the audio library on the right side -->
        <div class="library">
            <h3 class="list-title">Audio Library</h3>
            <!-- Searching Box -->
            <div class="flex-container">
              <form class="d-flex" @submit.prevent="searchAudio">
                <input class="searching-bar" type="search" placeholder="Search Audio" aria-label="Search" v-model="searchQuery" @input="searchAudio">
              <!-- Use drop-down boxes instead of search buttons -->
              <el-select v-model="selectedSearchField" placeholder="Search Field" class="orange-button" style="margin-top: 30px; margin-left: 10px; width: 300px">
                <el-option label="Search for All" value="all"></el-option>
                <el-option label="Search for Title" value="title"></el-option>
                <el-option label="Search for Type" value="type"></el-option>
                <el-option label="Search for Description" value="description"></el-option>
                <el-option label="Search for Grade" value="grade"></el-option>
                <!-- ... -->
              </el-select>
              </form>
              <button @click="openModal" class="orange-button margin_around" style="width: 150px">
                <i class="fas fa-plus fa-lg"></i> Add Audio
              </button>
              <button @click="editMode" class="orange-button margin_around" style="width: 150px; margin-right: 20px">
                <i class="fas fa-pencil-alt fa-lg"></i> Edit Mode
              </button>
            </div>
            <!-- dialog for add new audio to the library -->
            <div v-if="showModal" class="modal">
              <div class="modal-content">
                <span @click="closeModal" class="close">&times;</span>
                <!-- add new audio form -->
                <form @submit.prevent="saveAudio" class="form-container">
                  <label for="title">Title:</label>
                  <input v-model="addAudio.title" id="title" required>
                  <label for="file">Audio File:</label>
                  <div class="input-group">
                    <input type="file" ref="fileInput" @change="handleFileChange" id="file" required accept=".wav, .mp3, .mp4">
                  </div>
                  <label for="type">Type:</label>
                  <el-select v-model="addAudio.type" id="type" placeholder="Select Type" required>
                    <el-option label="Heartbeat" value="Heartbeat"></el-option>
                    <el-option label="Lungsound" value="Lungsound"></el-option>
                  </el-select>
                  <label for="description">Description:</label>
                  <textarea v-model="addAudio.description" id="description" required></textarea>
                  <label for="grade">Grade:</label>
                  <el-select v-model="addAudio.grade" id="grade" placeholder="Select Grade" required>
                    <el-option label="Primary" value="Primary"></el-option>
                    <el-option label="Intermediate" value="Intermediate"></el-option>
                    <el-option label="Advance" value="Advance"></el-option>
                  </el-select>
                  <button type="submit" class="save-button" style="display: block; margin-top: 10px; margin-left: 150px;">Save</button>
                </form>
              </div>
            </div>
            <!-- dialog for edit the existed audio in the library -->
            <div v-if="showModalEdit" class="modal">
              <div class="modal-content">
                <span @click="closeModalEdit" class="close">&times;</span>
                <!-- Edit Audio List Table -->
                <form @submit.prevent="editAudioContent" class="form-container">
                  <label for="title">Title:</label>
                  <div class="input-group">
                    <input v-model="editAudio.title" id="title" required>
                  </div>
                  <label for="link">Audio:</label>
                    <a :href="`http://127.0.0.1:8000/api/audioFile/${editAudio.link}/`"  target="_blank">{{ editAudio.link }}</a>
                  <label for="type">Type:</label>
                  <el-select v-model="editAudio.type" id="type" placeholder="Select Type" required>
                    <el-option label="Heartbeat" value="Heartbeat"></el-option>
                    <el-option label="Lungsound" value="Lungsound"></el-option>
                  </el-select>
                  <label for="description">Description:</label>
                  <textarea v-model="editAudio.description" id="description" required></textarea>
                  <label for="grade">Grade:</label>
                  <el-select v-model="editAudio.grade" id="grade" placeholder="Select Grade" required>
                    <el-option label="Primary" value="Primary"></el-option>
                    <el-option label="Intermediate" value="Intermediate"></el-option>
                    <el-option label="Advance" value="Advance"></el-option>
                  </el-select>
                  <div class="button-container-dialog">
                    <button type="submit" class="save-button" style="margin-left: 150px; margin-top: 10px;">Save</button>
                    <button type="button" @click="removeAudio" class="remove-button" style="margin-left: 50px; margin-top: 10px;">Remove</button>
                  </div>
                </form>
              </div>
            </div>
          <div class="library-table">
            <table>
              <thead>
                <tr>
                  <th style="width: 50px;">Add to list</th>
                  <th class="title th-clickable" @click="sortLibrary('title')">Title</th>
                  <th class="type th-clickable" @click="sortLibrary('type')">Type</th>
                  <th class="description th-clickable" @click="sortLibrary('description')">Description</th>
                  <th class="grade th-clickable" @click="sortLibrary('grade')">Grade</th>
                  <th v-if="editButton" style="width: 50px;">Edit</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="audio in audioLibrary" :key="audio.id">
                  <td>
                    <el-button
                      @click="addToList(audio)"
                      :class="{'add-to-list-button': isAudioInCurrentList(audio), 'applied': isAudioInCurrentList(audio)}"
                    >
                      <i class="fas fa-arrow-left" style="font-size: 2em;"></i>
                    </el-button>
                  </td>
                  <td>{{ audio.title }}</td>
                  <td>
                    <i :class="getIconClass(audio.type)"></i>
                  </td>
                  <td>{{ audio.description }}</td>
                  <td>{{ audio.grade }}</td>
                  <td v-if="editButton">
                    <el-button @click="() => openModalEdit(audio)" class="orange-button">
                      <i class="fas fa-edit" style="font-size: 2em;"></i>
                    </el-button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ElSelect, ElOption } from 'element-plus';
import { debounce } from 'lodash';

export default {
  components: {
    ElSelect,
    ElOption,
  },
  data() {
    return {
      list_url: 'http://localhost:8000/api/audioList/',
      listName: '',
      listId: '',
      sortColumn: 'title', // Default sorting column is 'title'
      sortDirection: 'asc', // Default sorting direction is 'asc' (ascending)
      isPlaying: false,
      loop: false,
      currentTime: 0,
      duration: 0,
      addAudio: {
        title: 'Song Title',
        link: 'Song Link',
        type: 'Type',
        description: 'Description',
        grade: 'Grade',
      },
      editAudio: {
        title: 'Song Title',
        link: 'Song Link',
        type: 'Type',
        description: 'Description',
        grade: 'Grade',
      },
      audioLibrary: [],
      searchAudioLibrary: [],
      availableLists: [],
      selectedListId: 1,
      heartapplied: false,
      lungsapplied: false,
      searchQuery: '',
      showModal: false,
      editButton: false,
      showModalEdit: false,
      //for add audio dialog
      selectedId: '',
      //for select search field
      selectedSearchField: 'all',
      debouncedSearchAudio: debounce(this.searchAudio, 300), // 300ms debounce for function serchAudio
    };
  },
  watch: {
    // For update the value of addAudio based on the selected title
    selectedId(id) {
      const selectedAudio = this.audioLibrary.find(audio => audio.id === id);
      if (selectedAudio) {
        // Update the values of addAudio
        this.editAudio.title = selectedAudio.title;
        this.editAudio.link = selectedAudio.link;
        this.editAudio.type = selectedAudio.type;
        this.editAudio.description = selectedAudio.description;
        this.editAudio.grade = selectedAudio.grade;
      }
    },
  },

  computed: {
    // For getting the current list based on the selected list id
    currentList() {
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      return selectedList ? selectedList.songs : [];
    },
  },

  methods: {
    //Current List --- Function called when press the create new list button
    async addNewList() {
      // Generate a default list name based on the length of availableLists
      const defaultListName = `list ${this.availableLists.length + 1}`;
      // Use the generated default name or prompt for a new name
      let newListName = prompt(`Enter the name for the new list (default: ${defaultListName}):`) || defaultListName;
      if(newListName == defaultListName){
        ElMessage.warning('Fail to creat new list!');
        return
      }

      // Remove consecutive spaces from the input name
      newListName = newListName.replace(/\s+/g, ' ');
      // Trim extra spaces from the input name
      newListName = newListName.trim();
      // Check if the new list name already exists
      const isNameTaken = this.availableLists.some(list => list.name === newListName);
      if (isNameTaken) {
        // If the name is taken, prompt the user to enter a different name
        ElMessage.error('List name already exists. Please choose a different name.');
        return;
      }
      //backend part...
      this.listName = newListName;
      // Transform the frontend availableList into the form suitable for the backend
      try {
        await axios.post(this.list_url, {
          list_name: this.listName,
        });
        // Wait for the backend to return the new list id
        this.getAll();
      } catch (error) {
        console.error('Error updating list on the backend:', error);
      }
        },

    //Current list --- Function to Sort Current Table
    sortTable(column) {
      if (column === this.sortColumn) {
        // If the same column is clicked again, reverse the sort direction
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // If a different column is clicked, set it as the new sorting column
        this.sortColumn = column;
        this.sortDirection = 'asc'; // Default to ascending order for the new column
      }
      // Sort the current list based on the selected column and direction
      this.currentList.sort((a, b) => {
        const aValue = a[column];
        const bValue = b[column];

      // Use localeCompare for string comparison, handle numbers and other types accordingly
      return this.sortDirection === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
      });
    },
    //Audio library --- Function to Sort Current Table
    sortLibrary(column) {
      if (column === this.sortColumn) {
        // If the same column is clicked again, reverse the sort direction
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // If a different column is clicked, set it as the new sorting column
        this.sortColumn = column;
        this.sortDirection = 'asc'; // Default to ascending order for the new column
      }

      // Sort the current list based on the selected column and direction
      this.audioLibrary.sort((a, b) => {
        const aValue = a[column];
        const bValue = b[column];

      // Use localeCompare for string comparison, handle numbers and other types accordingly
      return this.sortDirection === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
      });
    },

    //Current list --- Function called when press the rename list button
    renameList() {
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      if (selectedList) {
        // Prompt user for the new name
        let newName = prompt('Enter the new name for the list:', selectedList.name);
        // Remove consecutive spaces from the new name
        newName = newName.replace(/\s+/g, ' ');
        // Trim extra spaces from the beginning and end of the new name
        newName = newName.trim();
        // Check if the new name is the same as the old name or if it already exists
        if (newName && newName !== selectedList.name) {
          const isNameTaken = this.availableLists.some(list => list.name.trim() === newName);
          if (isNameTaken) {
            // If the name is taken, prompt the user to enter a different name
            ElMessage.error('List name already exists. Please choose a different name.');
            return;
          }
          const list_name_before = selectedList.name;
          // Update the name of the selected list
          selectedList.name = newName;
          const list_name_after = selectedList.name;
          // Update the backend
          this.listName = this.getCurrentListName();
          this.listId = this.selectedListId;
          //update the corresponding list content
          axios.delete(`http://localhost:8000/api/updateListContent/${list_name_before}/${list_name_after}`)
          // Update the list name
          axios.put(this.list_url + this.listId + '/', {
            list_id: this.listId,
            list_name: this.listName,
          })
          .then(() => {
            console.log('List updated successfully on the backend!');
            ElMessage.success('List name updated successfully!');
          })
          .catch(error => {
            console.error('Error updating list on the backend:', error);
          });
        }
      }
    },

    //Current list --- Function called when press the remove list button
    removeList(){
      if (this.availableLists.length > 1) {
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      if (selectedList) {
        const confirmation = confirm('Are you sure you want to remove this list?');
        if (confirmation) {
          const listName = this.getCurrentListName();
          for (const song of selectedList.songs) {
          // Make an API call to delete the association in the backend
          axios.delete(`http://localhost:8000/api/deleteListContent/${listName}/${song.title}`)
            .catch(error => {
              console.error('Error removing association from backend:', error);
              ElMessage({
                message: 'Error removing association. Please try again.',
                type: 'error',
              });
            });
          }
          const index = this.availableLists.findIndex(list => list.id === this.selectedListId);
          this.availableLists.splice(index, 1);
          //backend part...
          axios.delete(this.list_url + this.selectedListId + '/')
          this.selectedListId = this.availableLists[0].id; // Select the first list after removal
          ElMessage.success('List removed successfully!');
        }
      }
      } else {
        ElMessage.error('Oops, you can not remove the last list!')
      }
    },

    //Current List --- Function called when press the previous or next button beside the list selector
    navigateLists(direction) {
      const currentIndex = this.availableLists.findIndex(list => list.id === this.selectedListId);

      if (direction === 'prev' && currentIndex > 0) {
        this.selectedListId = this.availableLists[currentIndex - 1].id;
      } else if (direction === 'next' && currentIndex < this.availableLists.length - 1) {
        this.selectedListId = this.availableLists[currentIndex + 1].id;
      }
    },

    //Current List --- Function called for showing the current list name inside the list selector
    getCurrentListName() {
      const currentList = this.availableLists.find(list => list.id === this.selectedListId);
      return currentList ? currentList.name : 'Unknown List';
    },

    //Audio Library --- Function called when press the add to list button for adding the audio to the current list
    addToList(song) {
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      if (selectedList) {
        // Check if the song is not already in the current list
        const exists = selectedList.songs.some(item => item.id === song.id);
        // If the song does not exist in the current list, add it
        if (!exists) {
          // Add the new audio
          selectedList.songs.push({ ...song, applied: false });
        } else {
          alert('This audio already exists in the list!');
          return;
        }
        const endpoint = 'http://localhost:8000/api/listContent/';
        const listId = this.selectedListId;
        const listName = this.getCurrentListName();
        const audioId = song.id;
        const audioName = song.title;
        const requestData = {
          list_id: listId,
          list_name: listName,
          audio_id: audioId,
          audio_name: audioName,
        };
        axios.post(endpoint, requestData)
          .then(response => {
            console.log(response);
            ElMessage.success('Added Successfully!');
          })
          .catch(error => {
            console.error('Error saving audio data:', error);
            ElMessage.error('Error saving list content. Please try again.');
          })
      }
    },

    //Current List --- Function called when save list content to the backend
    saveListContent(){
      // save the current list content to the backend database
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      const listName = this.getCurrentListName();
      if (selectedList) {
        const endpoint = 'http://localhost:8000/api/listContent/';
        const promises = [];
        for (const audio of selectedList.songs) {
          const requestData = {
            list_name: listName,
            audio_name: audio.title,
          };
          // Using axios.post instead of axios.get for sending data
          promises.push(
            axios.post(endpoint, requestData)
              .then(response => {
                console.log(response);
              })
              .catch(error => {
                console.error('Error saving audio data:', error);
              })
          );
        }
        // Wait for all promises to resolve
        Promise.all(promises)
          .then(() => {
            // All requests are successful
            ElMessage.success('List content saved successfully!');
          })
          .catch(() => {
            // At least one request failed
            ElMessage.error('Error saving list content. Please try again.');
          });
      }
    },
    //Current List --- & Audio Library For showing the correct icon for the audio type
    getIconClass(type) {
      // Define a mapping of type names to icon classes
      const iconMapping = {
        'Heartbeat': 'fas fa-heartbeat',
        'heartbeat': 'fas fa-heartbeat',
        'Lungsound': 'fas fa-lungs',
        'lungsound': 'fas fa-lungs',
      };

      // Return the corresponding icon class based on the type
      return iconMapping[type] || ''; // Return an empty string if no match found
    },

    //Current list --- Function called when press the apply button (the play button)
    apply(song) {
      // Find the current audio of the same type that is applied
      const currentAppliedAudio = this.currentList.find(item => item.type === song.type && item.applied);
      // Check if the clicked audio is already applied
      if (song.applied) {
        // Toggle off the applied status
        song.applied = false;

        // Reset the corresponding applied flag
        if (song.type === 'Heartbeat') {
          this.heartapplied = false;
        } else if (song.type === 'Lungsound') {
          this.lungsapplied = false;
        }
      } else {
        // Check if there is already applied audio of the same type
        if (currentAppliedAudio) {
          // Unapply the current audio of the same type
          currentAppliedAudio.applied = false;

          // Reset the corresponding applied flag
          if (currentAppliedAudio.type === 'Heartbeat') {
            this.heartapplied = false;
          } else if (currentAppliedAudio.type === 'Lungsound') {
            this.lungsapplied = false;
          }
        }

        // Apply the clicked audio
        song.applied = true;
        // Set the corresponding applied flag
        if (song.type === 'Heartbeat') {
          this.heartapplied = true;
        } else if (song.type === 'Lungsound') {
          this.lungsapplied = true;
        }
      }
      // update the current active audio in the backend
      const id = song.id;
      const list_id = this.selectedListId;
      console.log(list_id)
      if(song.type == 'Heartbeat'){
        //delete all the content in active heart audio in BE
        //add this song to the active heart audio in BE
        ///....
        axios.delete(`http://localhost:8000/api/updateActiveHeartAudio/${id}/${list_id}/`)
      }
      else if(song.type == 'Lungsound'){
        //delete all the content in active lung audio in BE
        //add this song to the active lung audio in BE
        ///....
        axios.delete(`http://localhost:8000/api/updateActiveLungAudio/${id}/${list_id}/`)
      }
    },

    //Audio library --- Function called when press the remove button to remove the audio from the current list
    remove(song) {
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      if (selectedList) {
        const index = selectedList.songs.findIndex(item => item.id === song.id);
        selectedList.songs.splice(index, 1);
        const listName = this.getCurrentListName();
      // Make an API call to delete the association in the backend
      axios.delete(`http://localhost:8000/api/deleteListContent/${listName}/${song.title}`)
        .catch(error => {
          console.error('Error removing association from backend:', error);
          ElMessage({
            message: 'Error removing association. Please try again.',
            type: 'error',
          });
        });
        ElMessage({
          message: 'Removed Successfully！',
          type: 'warning',
        })
      }
    },

    //Current List --- Function for checking if the audio is in the current list
    isAudioInCurrentList(audio) {
      const selectedList = this.availableLists.find(list => list.id === this.selectedListId);
      return selectedList ? selectedList.songs.some(item => item.id === audio.id) : false;
    },

    //Current List & Audio Library ---  Function for getting all the audio from the database
    getAllAudio(resolve){
      this.audioLibrary = [];
      this.searchAudioLibrary = [];
      axios.get('http://localhost:8000/api/getAllAudio/')
      .then(response => {
        for (let audio of response.data) {
          // Push each audio object to audioLibrary array
          this.audioLibrary.push({
            id: audio.audio_id, // You can use a unique identifier as the id
            title: audio.audio_name,
            type: audio.audio_type,
            description: audio.audio_description,
            grade: audio.audio_level,
            link: audio.audio_link,
          });
          this.searchAudioLibrary.push({
            id: audio.audio_id, // You can use a unique identifier as the id
            title: audio.audio_name,
            type: audio.audio_type,
            description: audio.audio_description,
            grade: audio.audio_level,
            link: audio.audio_link,
          });
        }
        //alert(this.audioLibrary);
      })
      .catch(error => {
          console.error('Error fetching audio data:', error);
      })
      // Call resolve when the function is done
      resolve();
    },

    //Current List --- Function for getting all the audio list from the database
    getAllList(resolve){
      this.availableLists = [];
      axios.get('http://localhost:8000/api/getAllList/')
      .then(response => {
        this.availableLists = response.data.map(list => {
          return {
            id: list.list_id,
            name: list.list_name,
            songs: []  // Initialize songs as an empty array
          };
        });
          // Check if availableLists is not empty
        if (this.availableLists.length > 0) {
          // Set the selectedListId to the ID of the first list
          this.selectedListId = this.availableLists[0].id;
        }
      })
      .catch(error => {
        console.error('Error fetching audio data:', error);
      });
      // Call resolve when the function is done
      resolve();
    },

    //Current List --- Function for getting all the audio list content from the database
    getAllContent(resolve){
      axios.get('http://localhost:8000/api/listContent/')
      .then(response => {
        console.log('Received data from the server:', response.data);
        for (let content of response.data) {
          // Find the list that the content belongs to
          const list = this.availableLists.find(list => list.id === content.list_id);
          console.log('Found list:', list);
          const audio = this.audioLibrary.find(audio => audio.id === content.audio_id);
          console.log('Found audio:', audio);
          // console.log(audio.id)
          // console.log(audio.title)
          if (list && audio) {
            // Push the content to the list's songs array
            console.log('Adding content to list:', list.id);
            list.songs.push({
              id: audio.id,
              title: audio.title,
              type: audio.type,
              description: audio.description,
              grade: audio.grade,
              link: audio.link,
              applied: false,
            });
          }
        }
      })
      .catch(error => {
        console.error('Error fetching audio data:', error);
      });
      // Call resolve when the function is done
      resolve();
    },

    //Current List & Audio Library ---  Function for getting all the info
    getAll() {
      // Wrap each function in a Promise
      const getAllAudioPromise = () => new Promise(resolve => this.getAllAudio(resolve));
      const getAllListPromise = () => new Promise(resolve => this.getAllList(resolve));
      const getAllContentPromise = () => new Promise(resolve => this.getAllContent(resolve));

      // Define an async function to execute the promises sequentially
      const executeSequentially = async () => {
        await getAllAudioPromise();
        await getAllListPromise();
        await getAllContentPromise();
        this.loading = false; // Set loading to false after all data is fetched
      };

      // Call the async function
      executeSequentially();
    },
    
    //Audio Library --- Function for searching the audio
    filteredAudioLibrary() {
      const searchQuery = this.searchQuery.trim().toLowerCase();
      console.log('searchQuery:', searchQuery);
      if (!searchQuery) {
        ElMessage.warning("Please input something to search")
        return this.audioLibrary;
      }
      ElMessage.success("ready to search")
      this.audioLibrary.find(audio => audio.title.toString().toLowerCase().includes(searchQuery));
      this.searchAudioLibrary = this.audioLibrary.find(audio => {
        return (
          (audio.title && audio.title.toString().toLowerCase().includes(searchQuery))
        );
      });
    },
    //Audio Library --- For searchinq audio
    searchAudio() {
      // Actual search logic, modified as needed
      const searchQuery = this.searchQuery.trim().toLowerCase();
      console.log('Searching for:', searchQuery);
      if (!searchQuery) {
        // If the search criteria is empty, you can display all content or clear the search results
        console.log('Search query is empty, showing all audio');
        this.audioLibrary = [...this.searchAudioLibrary];
      } else {
        // Perform a search operation and update audioLibrary
        if(this.selectedSearchField == 'all'){
          this.audioLibrary = this.searchAudioLibrary.filter(audio => {
            return (
              (audio.title && audio.title.toString().toLowerCase().includes(searchQuery))||
              (audio.type && audio.type.toString().toLowerCase().includes(searchQuery))||
              (audio.description && audio.description.toString().toLowerCase().includes(searchQuery))||
              (audio.grade && audio.grade.toString().toLowerCase().includes(searchQuery))
            );
          });
        }
        else if(this.selectedSearchField == 'title'){
          this.audioLibrary = this.searchAudioLibrary.filter(audio => {
            return (
              (audio.title && audio.title.toString().toLowerCase().includes(searchQuery))
            );
          });
        }
        else if(this.selectedSearchField == 'type'){
          this.audioLibrary = this.searchAudioLibrary.filter(audio => {
            return (
              (audio.type && audio.type.toString().toLowerCase().includes(searchQuery))
            );
          });
        }
        else if(this.selectedSearchField == 'description'){
          this.audioLibrary = this.searchAudioLibrary.filter(audio => {
            return (
              (audio.description && audio.description.toString().toLowerCase().includes(searchQuery))
            );
          });
        }
        else if(this.selectedSearchField == 'grade'){
          this.audioLibrary = this.searchAudioLibrary.filter(audio => {
            return (
              (audio.grade && audio.grade.toString().toLowerCase().includes(searchQuery))
            );
          });
        }
      }
    },

    //Audio Library --- Function for dialog that adding new audio to the database
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      // Clear form data
      this.addAudio.title = 'Song title';
      this.addAudio.link = 'Song link';
      this.addAudio.type = 'Type';
      this.addAudio.description = 'Description';
      this.addAudio.grade = 'Grade';
      console.log('close add modal and reset data successfully!');
    },
    //Audio Library --- Function for dialog that edit exist audio in the database
    openModalEdit(audio) {
      // Set the selectedId to the current audio's title
      this.selectedId = audio.id;
      this.editAudio.id = audio.id;
      this.editAudio.title = audio.title;
      this.editAudio.link = audio.link;
      this.editAudio.type = audio.type;
      this.editAudio.description = audio.description;
      this.editAudio.grade = audio.grade;
      this.showModalEdit = true;
    },
    closeModalEdit() {
      this.showModalEdit = false;
      // Clear form data
      this.editAudio.title = 'Song title';
      this.editAudio.link = 'Song link';
      this.editAudio.type = 'Type';
      this.editAudio.description = 'Description';
      this.editAudio.grade = 'Grade';
      console.log('close edit modal and reset data successfully!');
    },
    // Audio Library --- Function for saving a NEW audio to the database
    handleFileChange(){
      // Called when the file selection changes
      // Get file object and store in component data
      this.addAudio.file = this.$refs.fileInput.files[0];
    },
    saveAudio() {
      // To add new audio into the library
      console.log("Testing");

      // Check whether title has special characteristics
      const specialCharRegex = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>?]+/;
      if (specialCharRegex.test(this.addAudio.title)) {
        alert('Title contains special characters.');
        return;
      }
      // Check whether title, link, type, grade have been filled
      if (!this.addAudio.title || !this.addAudio.link || !this.addAudio.type || !this.addAudio.grade) {
        alert('Please fill in all required fields.');
        ElMessage.warning('Please fill in all required fields.');
        return;
      }
      if(this.addAudio.title == 'Song Title' || !this.addAudio.file || this.addAudio.type == 'Type' || this.addAudio.grade == 'Grade'){
        alert('Please fill in all required fields.');
        ElMessage.warning('Please fill in all required fields.');
        return;
      }
      this.uploadFile();
    },
    // Handle file uploading in save audio
    uploadFile(){
      const fileInput = this.$refs.fileInput;
      const file = fileInput.files[0];

      // Use FormData to build the file upload
      const formData = new FormData();
      formData.append('file', file);

      // Send the file to the backend
      axios.post('http://localhost:8000/api/uploadAudio/', formData)
      .then(response => {
        // Once file is successfully uploaded, proceed to save audio information
        console.log('File uploaded successfully:', response.data);
      // Assuming the backend returns the uploaded filename
      // Continue with saving audio information to the backend
        const addData = {
          audio_name: this.addAudio.title,
          audio_type: this.addAudio.type, 
          audio_description: this.addAudio.description,
          audio_level: this.addAudio.grade,
          audio_link: response.data.filename.replace('audio/', ''),//Remove the 'audio/' prefix
        };

        // Send audio information to the backend
        axios.post('http://localhost:8000/api/audio/', addData)
        .then(response => {
          console.log('Audio saved successfully:', response.data);
          this.showModal = false;
          this.getAll();  // Assuming you have a method to fetch all audio after adding a new one
          ElMessage.success('New audio added successfully!');
        })
        .catch(error => {
          console.error('Error saving audio:', error);
        });
      })
        .catch(error => {
          // Handle file upload error
          console.error('File upload failed:', error);
        });
    },
    //Audio Library --- Function for showing or hiding the edit buttons for each audio
    editMode() {
      this.editButton = !this.editButton;
    },
    //Audio Library --- Function for edit a existed audio in the database
    async editAudioContent() {
      try {
        // Update the corresponding audio in the audioLibrary
        const index = this.audioLibrary.findIndex(audio => audio.id === this.selectedId);

        if (index !== -1) {
          // Update the properties of the corresponding audio with the edited values
          this.audioLibrary[index] = { ...this.audioLibrary[index], ...this.editAudio };
                // Include the updated data in the request
          const updatedData = {
            audio_id: this.editAudio.id,
            audio_name: this.editAudio.title,
            audio_type: this.editAudio.type, 
            audio_description: this.editAudio.description,
            audio_level: this.editAudio.grade,
            audio_link: this.editAudio.link,
          };
          // Send the updated audio data to the backend
          const response = await axios.patch(`http://127.0.0.1:8000/api/audio/${this.audioLibrary[index].id}/update_audio_property/`, updatedData);

          // You can handle the response from the server if needed
          console.log('Audio updated successfully', response.data);
        }
      } catch (error) {
        // Handle any errors that occurred during the API request
        console.error('Error updating audio', error);
      }
      ElMessage.success('Change saved Successfully!');
      ElMessage.warning('Loading...');
      this.getAll();
      this.selectedId = '';
      this.closeModalEdit();
    },
    //Audio Library --- Function for remove a existed audio in the database
    async removeAudio() {
      try {
        // Find the index of the audio to be removed
        const index = this.audioLibrary.findIndex(audio => audio.id === this.selectedId);
        if (index !== -1) {
          // Send a request to delete the audio from the backend
          await axios.delete(`http://127.0.0.1:8000/api/audio/${this.audioLibrary[index].id}/delete_audio/`);
          console.log('Audio info removed successfully');
          await axios.delete(`http://127.0.0.1:8000/api/deleteRelatedListContent/${this.audioLibrary[index].id}`);
          console.log('List content removed successfully');
          await axios.delete(`http://127.0.0.1:8000/api/audioFile/${this.audioLibrary[index].link}/delete_audio_file/`);
          console.log('Audio file removed successfully');

          // Remove the audio from the local audioLibrary
          this.audioLibrary.splice(index, 1);
        }
        ElMessage.success('Removed Successfully!');
      } catch (error) {
        // Handle any errors that occurred during the API request
        console.error('Error removing audio', error);
        ElMessage.error('Error removing audio. Please try again.');
      }
      ElMessage.warning('Loading...');
      this.getAll();
      this.selectedId = '';
      this.closeModalEdit();
    },
  },
  created() {
    ElMessage.warning('Loading, please wait...');
    this.getAll();
  },
};
</script>

<style scoped>
.audio-player {
  background-color: white;
  color: black;
}

.list-title {
  text-align: center;
  justify-content: space-between;
  color: #e64626;
  font-size: 30px;
}

.lists {
  display: flex;
  justify-content: space-between;
}
.lists table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.lists th,
.lists td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.lists th {
  position: sticky;
  top: 0;
  z-index: 1; /* Ensure that the header is always at the top when scrolling */
  background-color: #424242;
  color: white;
}

.th-clickable:hover {
  background-color: #f2f2f2; /* add hold over colour changing */
  cursor: pointer;
  color: #333;
}

.lists th.title {
  width: 120px; /* Width of title column */
}
.lists th.type {
  width: 100px; /* Width of type column */
}
.lists th.description {
  width: 200px; /* Describe the width of the column */
}
.lists th.grade {
  width: 80px; /* Width of level column */
}
.lists th.apply {
  width: 100px; /* Apply column width */
}
.lists th.remove {
  width: 100px; /* Remove column width */
}

.applied {
  background-color: green;
  color: white;
  height: 40px;
}
.green-button {
  background-color: green;
  color: white;
}

.space-between {
  width: 20px;
}

.margin_around{
  margin-left: 100px;
  margin-top: 30px;
}

.current-list-title{
  font-size: 20px;
}
.current-list-table{
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  margin-left: 10px;
  text-align: center;
}

.listSelector{
  width: 200px;
  height: 30px;
  font-size: 20px;
  text-align: center;
  margin-right: 10px;
  margin-left: 10px;
}

.button-container{
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
  gap: 10px;
}
.library-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  max-height: 600px; /* Set the maximum height. If the height exceeds this height, a scroll bar will appear */
  overflow-y: auto; /* Set vertical scroll bar */
}

.add-to-list-button {
  background-color: #e64626; /* Orange color */
  color: #fff; /* White text color */
  border: none;
  padding: 8px;
  cursor: default;
}

.orange-button {
  background-color: #e64626; /* Orange color */
  color: #fff; /* White text color */
  border: none;
  padding: 8px;
  cursor: pointer;
}

.orange-button:hover {
  background-color: #F90; /* Darker orange on hover */
}

.black-button {
  background-color: #424242; /* Black color */
  color: #fff; /* White text color */
  border: none;
  padding: 8px;
  cursor: pointer;
}

.black-button:hover {
  background-color: #424242; /* Darker black on hover */
}
/* Searching bar */
.d-flex {
  display: flex;
  align-items: center;
}

.searching-bar {
  margin-top: 45px;
  padding: 8px;
  border: 1px solid #e64626; /* Orange border */
  border-radius: 4px;
  outline: none;
  font-size: 16px;
  color: #424242; /* Black text */
  background-color: #fff; /* White background */
}

/* Add hover effect */
.searching-bar:hover {
  border-color: #F90; /* Darker orange on hover */
}

/* Add focus effect */
.flex-container{
  display: flex;
  align-items: center;
}
.searching-bar:focus {
  border-color: #e64626; /* Even darker orange on focus */
  box-shadow: 0 0 8px rgba(255, 153, 0, 0.4); /* Orange box shadow on focus */
  background-color: #fff; /* White background on focus */
}
/* Adding audio to library dialog */
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
  background-color: #252525;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  position: relative;
}

.close {
  color: #e64626;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
}

form {
  color: #e64626;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #f90;
  border-radius: 5px;
  background-color: #252525;
  color: #e64626;
}

.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.input-group input {
  flex: 1;
  padding: 8px;
}

.input-group button {
  padding: 8px 12px;
  background-color: #e64626;
  color: #252525;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.input-group button:hover {
  background-color: #e64626;
}
/* for dialog button */
.button-container-dialog {
  display: flex;
  margin-top: 10px;
}

.save-button {
  background-color: #e64626;
  color: #252525;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 10px; /* Adjust the distance between buttons */
}

.remove-button {
  background-color: #e64626;
  color: #252525;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-left: 10px; /* Adjust the distance between buttons, or set margin-left directly */
}

.save-button:hover {
  background-color: #e64626;
}
</style>