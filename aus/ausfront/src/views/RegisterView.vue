<template>
  <div class="registration-container">
    <div class="tabs">
      <div :class="{ active: activeTab === 'school' }" @click="setActiveTab('school')">School Registration</div>
      <div :class="{ active: activeTab === 'personal' }" @click="setActiveTab('personal')">Personal Registration</div>
    </div>

    <div v-if="activeTab === 'school'" class="registration-form active">
      <h2 style="color: #e64626; text-align: center;">School Registration</h2>
      <form @submit.prevent="registerSchool">
        <div class="form-group">
          <label for="schoolUsername">School Username:</label>
          <input type="text" id="schoolUsername" v-model="schoolUsername" placeholder="Enter your school username" required />
        </div>
        <div class="form-group">
          <label for="schoolPassword">School Password:</label>
          <input type="password" id="schoolPassword" v-model="schoolPassword" placeholder="Enter your school password" required />
        </div>
        <button type="submit" style="background-color: #e64626; color: #fff;">Register</button>
      </form>
    </div>

    <div v-else class="registration-form active">
      <h2 style="color: #e64626; text-align: center;">Personal Registration</h2>
      <form @submit.prevent="registerPersonal">
        <div class="form-group">
          <label for="personalEmailOrPhone">Email or Phone:</label>
          <input type="text" id="personalEmailOrPhone" v-model="personalEmailOrPhone" placeholder="Enter your email or phone to start" required />
        </div>
        <div class="form-group">
          <label for="personalPassword">Password:</label>
          <input type="password" id="personalPassword" v-model="personalPassword" placeholder="Enter your password for safety reason" required />
        </div>
        <div class="form-group">
          <label for="repeatPersonalPassword">Repeat Password:</label>
          <input type="repeatPassword" id="repeatPersonalPassword" v-model="repeatPersonalPassword" placeholder="Enter your password again to make sure everything is fine" required />
        </div>
        <div class="form-group">
          <label for="personalNickname">Prefer Name:</label>
          <input type="text" id="personalNickname" v-model="personalNickname" placeholder="Enter your nickname and no real name needed" required />
        </div>
        <button type="submit" style="background-color: #e64626; color: #fff;">Register</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.registration-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
}

.tabs div {
  flex: 1;
  padding: 10px;
  cursor: pointer;
  background-color: #e0e0e0;
}

.tabs div.active {
  background-color: #e64626;
  color: #fff;
}

.registration-form {
  display: none;
}

.registration-form.active {
  display: block;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  cursor: pointer;
  border: none;
  padding: 10px;
  border-radius: 5px;
}

button:hover {
  background-color: #e78a4e;
}
</style>

<script>
export default {
  data() {
    return {
      activeTab: 'school',
      schoolUsername: '',
      schoolPassword: '',
      personalEmailOrPhone: '',
      personalPassword: '',
      repeatPersonalPassword: '',
      personalNickname: '',
    };
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    async registerSchool(){
      try{
        const Response = await this.$http.post('/api/registerSchool', {
          username: this.schoolUsername,
          password: this.schoolPassword
        });
        console.log('School Registration Successful:', Response.data);
      }catch(error){
        console.log('School Registration Failed:', error);
      } 
    },
    async registerPersonal(){
      if(this.personalPassword !== this.repeatPersonalPassword){
        return alert('Password does not match!');
      }
      else if(this.personalPassword.length < 6){
        return alert('Password must be at least 6 characters!');
      }
      else if(this.personalNickname.length < 3){
        return alert('Nickname must be at least 3 characters!');
      }
      else if(this.personalNickname.length > 20){
        return alert('Nickname must be less than 20 characters!');
      }
      else if(!this.personalEmailOrPhone.includes('@') && !this.personalEmailOrPhone.includes('.')){
        return alert('Email or Phone is invalid!');
      }
      else{
        try{
          const Response = await this.$http.post('/api/registerPersonal', {
            emailOrPhone: this.personalEmailOrPhone,
            password: this.personalPassword,
            nickname: this.personalNickname
          });
          console.log('Personal Registration Successful:', Response.data);
        }catch(error){
          console.log('Personal Registration Failed:', error);
        }
      }
    },
  }
};
</script>
