<template>
    <div class="login-container">
      <h2 style="color: #e64626;">Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username" style="color: #666;">Username:</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="password" style="color: #666;">Password:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" style="background-color: #e64626; color: #fff;">Login</button>
      </form>
      <div class="register-link" style="color: #666;">
        <router-link to="/register" style="color: #e64626;">Don't have an account? Register here.</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      login() {
        // Handle login logic here
        console.log('Logging in with:', this.username, this.password);
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    text-align: center; /* Center the content horizontally */
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
    background-color: #e64626;
  }
  
  .register-link {
    margin-top: 10px;
    text-align: center;
  }
  
  .register-link a {
    text-decoration: none;
  }
  
  .register-link a:hover {
    text-decoration: underline;
  }
  </style>
  