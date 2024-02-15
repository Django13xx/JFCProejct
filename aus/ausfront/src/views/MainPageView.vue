<template>
  <div class="listening-app">
    <div class="list-info">
      <p>Current list is: </p>
      <span>
        <select
          id="listSelector"
          class="listSelector"
          v-model="selectedListId"
          @change="loadSelectedList"
        >
          <option v-for="list in availableLists" :key="list.id" :value="list.id">
              {{list.name}}
          </option>
        </select>
      </span>
    </div>
    <div class="status-icons">
      <div class="icon heart-icon" :class="{ active: isHeartActive }" v-tooltip="'Show Heart Mode Status'">
        <i class="fas fa-heartbeat"></i>
      </div>
      <div class="icon lung-icon" :class="{ active: isLungActive }" v-tooltip="'Show Lung Mode Status'">
        <i class="fas fa-lungs"></i>
      </div>
    </div>
    <div class="control-panel">
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Play default audio sets in the teaching dashboard"
        placement="bottom-start"
      >
        <button @click="toggleActiveMode" class="active-btn">Default Mode</button>
      </el-tooltip>
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Swap current Heart Beat audio for different sounds to practice heart rate counting or others"
        placement="bottom-start"
      >
        <button @click="toggleHeartbeatMode" class="heartbeat-btn">Heartbeat Mode</button>
      </el-tooltip>
      <!-- Randomly use abnormal sounds for heart or lung, improving students' listening skills. -->
      <el-tooltip
        class="box-item"
        effect="dark"
        content="Randomly use abnormal sounds for Heart or Lung, improving students' listening skills."
        placement="bottom"
      >
        <button @click="toggleAbnormalSoundsMode" class="abnormal-btn" v-tooltip="'Abnormal Mode: Introduces random abnormalities in heart or lung sounds'">Abnormal Mode</button>
      </el-tooltip>
      <el-tooltip
        class="box-item"
        effect="dark"
        content="All audio randomly appears, providing a challenging simulation for practical auscultation training."
        placement="bottom-end"
      >
        <button @click="toggleMixedMode" class="mixed-btn" v-tooltip="'Mixed Mode: Randomly changes heart or lung sounds, may include abnormalities'">Random Mode</button>
      </el-tooltip>
    </div>
    <div class="interaction-area">
      <h3><input type="text" placeholder="Note Area..." style="width: 100%; height:fit-content"></h3>
    </div>
    <div class="audio-display">
      <div class="currently-playing-heart">
        <h3 v-if="currentHeart">Currently <i class="fas fa-heartbeat"></i>: </h3>
        <p v-if="currentHeart">{{ currentHeart.name }}</p>
        <h3 v-if="currentHeart">The link is:</h3>
        <p v-if="currentHeart"><a :href="getAudioUrl(currentHeart.link)" target="_blank">{{ currentHeart.link }}</a></p>
        <audio controls autoplay v-if="currentHeart">
          <source :src="getAudioUrl(currentHeart.link)" type="audio/wav">
          Your browser does not support the audio element.
        </audio>
      </div>
      <div class="currently-playing-lung">
        <h3 v-if="currentLung">Currently <i class="fas fa-lungs"></i>: </h3>
        <p v-if="currentLung">{{ currentLung.name }}</p>
        <h3 v-if="currentLung">The link is:</h3>
        <p v-if="currentLung"><a :href="getAudioUrl(currentLung.link)" target="_blank">{{ currentLung.link }}</a></p>
        <audio controls autoplay v-if="currentLung">
          <source :src="getAudioUrl(currentLung.link)" type="audio/wav">
          Your browser does not support the audio element.
        </audio>
      </div>
    </div>
    <div v-if="playHistory && playHistory.length > 0" class="history-area">
      <h3>Play History <button @click="clearHistory" class="clear-history"><i class="fas fa-trash-alt fa-lg"></i> Clear History</button></h3>      
      <ul>
        <li v-for="(history, index) in reversedHistory" :key="index">
          {{ history.name }} - <a :href="history.link" target="_blank">{{ history.link }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ref, onMounted  } from 'vue';
import io from 'socket.io-client';
export default {
  setup() {
    const analogReading = ref(0);
    const analogHistory = ref([]);
    const shouldToggleHeartMode = ref(false);
    const shouldToggleLungsMode = ref(false);
    const stopAll = ref(false);
    let stillHeart = false;
    let stillLungs = false; 
    let lastDataTimestamp = Date.now();


    // 处理接收到的数据
    const processData = (data) => {
      //console.log('Received data:', data);
      // 更新最后一次数据更新的时间戳
      lastDataTimestamp = Date.now();
      console.log("Last data timestamp: ", lastDataTimestamp);

      // 分析数据格式，如果匹配特定条件，触发HeartMode
      const matchedHeart = data.match(/S([01]) (\d+)/);
      const matchedLungs = data.match(/S([23]) (\d+)/);

      if (matchedHeart) {
        const sensorId = matchedHeart[1];
        console.log("HeartId: ", sensorId);
        analogHistory.value.push(matchedHeart[0]); // add to history
        // check if there is only the data osscilation between heart and lungs
        stillLungs = analogHistory.value.some(item => item === '2' || item === '3');
        // if no osscilation, then stop the lung mode
        if(!stillLungs){
          shouldToggleLungsMode.value = false;
        }
        // start heart mode
        shouldToggleHeartMode.value = true;

      } else if (matchedLungs) {
        const sensorId = matchedLungs[1];
        console.log("LungId: ", sensorId);
        analogHistory.value.push(matchedLungs[0]); // add to history
        // check if there is only the data osscilation between heart and lungs
        stillHeart = analogHistory.value.some(item => item === '0' || item === '1');
        // if no osscilation, then stop the heart mode
        if(!stillHeart){
          shouldToggleHeartMode.value = false;
        }
        // start lung mode
        shouldToggleLungsMode.value = true;
      }

      //console.log("History length: " + analogHistory.value.length);

      if (analogHistory.value.length >= 10) {
        analogHistory.value.shift(); // delete the first element
      }
      analogReading.value = data; // update the data
      //console.log("shouldToggleHeartMode: ", shouldToggleHeartMode.value," shouldToggleLungsMode: ", shouldToggleLungsMode.value);
    };

    // 定时检查最后一次数据更新的时间戳
    setInterval(() => {
      const currentTime = Date.now();
      const timeDiff = currentTime - lastDataTimestamp;

      // 如果一定时间内没有数据更新，说明没有持续的振荡
      if (timeDiff > 2000) { // 设置为你需要的时间间隔，单位为毫秒
        stopAll.value = true;
        shouldToggleHeartMode.value = false;
        shouldToggleLungsMode.value = false;  
      }
    }, 1000); // 设置为你需要的检查时间间隔，单位为毫秒

    onMounted(() => {
      const socket = io('http://localhost:3000');
      socket.on('data', processData);
      //console.log('level one');
    });

    return {
      analogReading,
      analogHistory,
      stopAll,
      shouldToggleHeartMode,
      shouldToggleLungsMode,
    };
  },
  data() {
    return {
      isHeartActive: false,
      isLungActive: false,
      audio_name:'',
      audio_link:'',
      currentList: null,
      currentHeart: null,
      currentLung: null,
      playHistory: [],
      availableLists: [],
      selectedListId: 1,
      mode0: false,
      mode1: false,
      mode2: false,
      mode3: false,
    };
  },
  computed: {
    reversedHistory() {
      // Reverse array order using Array.reverse()
      return this.playHistory.slice().reverse();
    }
  },
  methods: { 
    // For getting the avaliable list from the backend
    //Current List --- Function for getting all the audio list from the database
    getAllList(){
      this.availableLists = [];
      axios.get('http://localhost:8000/api/getAllList/')
      .then(response => {
        this.availableLists = response.data.map(list => {
          return {
            id: list.list_id,
            name: list.list_name,
            // activeheart:1,
            // activelung:2,
          };
        });
        // Check if availableLists is not empty
        if (this.availableLists.length > 0) {
          // Iterate through each list to fetch activeHeartAudio and activeLungAudio data
          this.availableLists.forEach(list => {
            // Fetch activeHeartAudio data
            axios.get(`http://localhost:8000/api/getActiveHeartAudio/${list.id}/`)
              .then(response => {
                // Update the activeheart property of the current list
                list.activeheart = response.data.audio_id;
              })
              .catch(error => {
                console.error(`Error fetching activeHeartAudio data for list ${list.id}:`, error);
              });

            // Fetch activeLungAudio data
            axios.get(`http://localhost:8000/api/getActiveLungAudio/${list.id}/`)
              .then(response => {
                // Update the activelung property of the current list
                list.activelung = response.data.audio_id;
                console.log("activelung: ", list.activelung , " list id: ", list.id);
              })
              .catch(error => {
                console.error(`Error fetching activeLungAudio data for list ${list.id}:`, error);
              });
          });
        }
      })
      .catch(error => {
        console.error('Error fetching audio data:', error);
      });
    },
    // For getting the audio url from the backend
    getAudioUrl(filename) {
      return `http://127.0.0.1:8000/api/audioFile/${filename}/`;
    },
    startPlaying() {
    // 设置 isHeartActive 状态
    this.isHeartActive = true;

    // 请求音频数据并播放
    const heartId = this.availableLists.find(list => list.id === this.selectedListId).activeheart;
    axios.get('http://localhost:8000/api/audio/' + heartId + '/')
      .then((response) => {
        const audio = response.data;
        this.currentHeart = {
          name: audio.audio_name,
          link: audio.audio_link,
        };
        // 播放音频
        this.playAudio(this.currentHeart.link);
        // 添加到播放历史
        this.playHistory.push(this.currentHeart);
      })
      .catch((error) => {
        console.error(error);
      });
  },

  stopPlaying() {
    // 停止播放音频并清除 currentHeart
    if (this.currentHeart && this.$refs.audioElement) {
      const audioElement = this.$refs.audioElement;
      audioElement.pause();
      audioElement.currentTime = 0; // 重置音频时间
    }
    this.currentHeart = null;
    this.isHeartActive = false;
    if(this.currentLung && this.$refs.audioElement) {
      const audioElement = this.$refs.audioElement;
      audioElement.pause();
      audioElement.currentTime = 0; // 重置音频时间
    }
    this.currentLung = null;
    this.isLungActive = false;
  },
    toggleHeartMode() {
      this.currentHeart = null
      this.isHeartActive = !this.isHeartActive;
      if(this.isHeartActive){
        const heartId = this.availableLists.find(list => list.id === this.selectedListId).activeheart;
        axios.get('http://localhost:8000/api/audio/' + heartId + '/')
        .then((response) => {
          console.log(response);
          const audio = response.data;
          this.audio_name = audio.audio_name;
          this.audio_link = audio.audio_link;
          console.log('audio_name:', audio.audio_name);
          console.log('audio_link:', audio.audio_link);
          this.currentHeart = {
            name: this.audio_name,
            link: this.audio_link,
          };
          console.log(this.currentHeart); // Output the data to the console
          // Add to play history
          this.playHistory.push({
              name: this.audio_name,
              link: this.audio_link,
          });
        })
        .catch((error) => {
          console.log(error);
        });
      }
      else{
        this.currentHeart = null;
      }
    },
    toggleLungsMode() {
      this.currentLung = null
      this.isLungActive = !this.isLungActive;
      if(this.isLungActive){
        const lungId = this.availableLists.find(list => list.id === this.selectedListId).activelung;
        axios.get('http://localhost:8000/api/audio/' + lungId + '/')
        .then((response) => {
          console.log(response);
          const audio = response.data;
          this.audio_name = audio.audio_name;
          this.audio_link = audio.audio_link;
          console.log('audio_name:', audio.audio_name);
          console.log('audio_link:', audio.audio_link);
          this.currentLung = {
            name: this.audio_name,
            link: this.audio_link,
          };
          console.log(this.currentLung); // Output the data to the console    
          // Add to play history
          this.playHistory.push({
              name: this.audio_name,
              link: this.audio_link,
          });
        })
        .catch((error) => {
          console.log(error);
        });
      }
      else{
        this.currentLung = null;
      }
    },
    toggleActiveMode(){
      this.mode0 = !this.mode0;
      this.mode1 = false;
      this.mode2 = false;
      this.mode3 = false;
      this.isHeartActive = false;
      this.isLungActive = false;
      this.currentHeart = null;
      this.currentLung = null;
      if(this.mode0 == true){
        this.toggleHeartMode();
        this.toggleLungsMode();
      }
    },
    toggleHeartbeatMode() {
      this.mode0 = false
      this.mode1 = !this.mode1
      this.mode2 = false
      this.mode3 = false
      this.currentLung = null
      if(this.mode1 == false)
        this.stopPlaying();
      else{
        this.currentHeart = null
        this.isHeartActive = true;
        this.isLungActive = false;
        const endpoint = 'http://localhost:8000/api/playRandomHeartBeat/';
        this.playHeart(endpoint);
      }
    },
    toggleAbnormalSoundsMode() {
      this.mode0 = false
      this.mode1 = false
      this.mode2 = !this.mode2;
      this.mode3 = false
      if(this.mode2 == false)
        this.stopPlaying();
      else{
        this.currentHeart = null
        this.currentLung = null
        this.isHeartActive = false;
        this.isLungActive = false;
        const endpoint = 'http://localhost:8000/api/playRandomAbnormal/';
        this.play(endpoint);
      }
    },
    toggleMixedMode() {
      this.mode0 = false
      this.mode1 = false
      this.mode2 = false
      this.mode3 = !this.mode3;
      if(this.mode3 == false)
        this.stopPlaying();
      else{
        this.currentHeart = null
        this.currentLung = null
        this.isHeartActive = false;
        this.isLungActive = false;
        const endpoint = 'http://localhost:8000/api/playRandom/';
        this.play(endpoint);
      }
    },

    // for play the random Heart audio get from the backend
    playHeart(endpoint){
      axios.get(endpoint)
      .then((response) => {
        console.log(response);
        this.audio_name = response.data.audio_name;
        this.audio_link = response.data.audio_link;
        console.log('audio_name:', response.data.audio_name);
        console.log('audio_link:', response.data.audio_link);

        this.currentHeart = {
          name: this.audio_name,
          link: this.audio_link,
        };
        console.log(this.currentHeart); // Output the data to the console
        // Add to play history
        this.playHistory.push({
            name: this.audio_name,
            link: this.audio_link,
        });
      })
    },
    
    // for play the random Lung audio get from the backend (Havent been used yet 12/01/2024)
    playLung(endpoint){
      axios.get(endpoint)
      .then((response) => {
        console.log(response);
        this.audio_name = response.data.audio_name;
        this.audio_link = response.data.audio_link;
        console.log('audio_name:', response.data.audio_name);
        console.log('audio_link:', response.data.audio_link);
        this.currentLung= {
          name: this.audio_name,
          link: this.audio_link,
        };
        console.log(this.currentLung); // Output the data to the console
        // Add to play history
        this.playHistory.push({
            name: this.audio_name,
            link: this.audio_link,
        });
      })
    },

    // for play the random audio get from the backend
    play(endpoint){
      axios.get(endpoint)
      .then((response) => {
        console.log(response);
        this.audio_name = response.data.audio_name;
        this.audio_type = response.data.audio_type;
        this.audio_link = response.data.audio_link;
        console.log('audio_name:', response.data.audio_name);
        console.log('audio_type:', response.data.audio_link);
        console.log('audio_link:', response.data.audio_link);
        if(this.audio_type == 'Heartbeat'){
          this.toggleLungsMode();
          this.isHeartActive = true;
          this.currentHeart = {
            name: this.audio_name,
            link: this.audio_link,
          };
          console.log(this.currentHeart); // Output the data to the console
        }
        else{
          this.toggleHeartMode();
          this.isLungActive = true;
          this.currentLung= {
            name: this.audio_name,
            link: this.audio_link,
          };
          console.log(this.currentLung); // Output the data to the console
        }
        // Add to play history
        this.playHistory.push({
            name: this.audio_name,
            link: this.audio_link,
        });
      })
    },

    clearHistory() {
      this.playHistory = [];
    },
  },
  created() {
    ElMessage.warning('Loading, please wait...');
    this.getAllList();
  },
  watch: {
    selectedListId(newListId, oldListId) {
      console.log('selectedListId changed from ', oldListId, ' to ', newListId); 
      if (this.isHeartActive)
        this.toggleHeartMode();
      if (this.isLungActive)
        this.toggleLungsMode();
    },
    shouldToggleHeartMode(newData, oldData){
      console.log(`new: ${newData}, old: ${oldData}`);
    if (newData !== oldData) {
      if (newData) {
        if (!this.isHeartActive) {
          this.toggleHeartMode();
        }
        if (this.isLungActive) {
          this.toggleLungsMode();
        }
      } else {
        this.toggleHeartMode();
      }
    }
    },
    shouldToggleLungsMode(newData, oldData){
      if(newData !== oldData && newData === true){
        if(!this.isLungActive){
          this.toggleLungsMode();
        }
        if(this.isHeartActive){
          this.toggleHeartMode();
        }
      }
      if(newData !== oldData && newData === false){
        this.toggleLungsMode();
      }
    },
    stopAll(newData, oldData){
      if(newData !== oldData && newData === true){
        if(this.isHeartActive){
          this.toggleHeartMode();
        }
        if(this.isLungActive){
          this.toggleLungsMode();
        }
      }
    }
  },
};
</script>

<style scoped>
.listening-app {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.list-info {
  display: flex;
  align-items: center;
}

.list-info p{
  margin-top: 20px;
  margin-bottom: 20px;
  margin-right: 20px;
}

.status-icons {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}

.icon {
  pointer-events: none;
  position: relative;
  width: 80px;
  height: 80px;
  margin-right: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 32px;
  cursor: pointer;
}

.heart-icon {
  background-color: #E41B17;
  color: #fff;
}

.lung-icon {
  background-color: #2196f3;
  color: #fff; 
}

.heart-icon.active {
  animation: blinkColorChangeHeart 1s infinite alternate;
}

.lung-icon.active {
  animation: blinkColorChangeLung 1s infinite alternate;
}

@keyframes blinkColorChangeHeart {
  0% {
    background-color: transparent;
    color: red;
  }
  100% {
    background-color: red;
    color: white;
  }
}

@keyframes blinkColorChangeLung {
  0% {
    background-color: transparent;
    color: blue;
  }
  100% {
    background-color: blue;
    color: white;
  }
}

.audio-display {
  display: flex;
  justify-content: space-between;
}

.currently-playing-heart,
.currently-playing-lung {
  width: 48%;
}

.control-panel button {
  margin: 0 10px;
  padding: 15px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

.active-btn {
  background-color: #2196f3;
  color: #fff; 
}

.heartbeat-btn {
  background-color: #4caf50;
  color: #fff; 
}

.abnormal-btn {
  background-color: #ff9800;
  color: #fff; 
}

.mixed-btn {
  background-color: #e64626; 
  color: #fff;
}

.interaction-area {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 70%;
}

.interaction-area h3 {
  margin-bottom: 10px;
}

.clear-history {
  margin-top: 50px;
  margin-bottom: 10px;
  background-color: #e64626; /* Orange color */
  color: #fff; /* White text color */
  border: none;
  padding: 8px;
  cursor: pointer;
  font-size: 10px; /* Adjust the font size as needed */
  border-radius: 5px; /* Add border-radius for rounded corners */
}
</style>
  