<template>
    <div class="login-container">
      <h2>Please enter the password:</h2>
      <input v-if="showInput" type="password" v-model="password" @keyup.enter="checkPassword" placeholder="password" autocomplete="new-password"/>
      <button @click="checkPassword">Yes!</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        password: '',
        errorMessage: '',
        showInput: true
      };
    },
    methods: {
      checkPassword() {
        const correctPassword = '123456'; // password
        if (this.password === correctPassword) {
          sessionStorage.setItem('authenticated', 'true'); // login state
          this.$router.push('/'); 
        } else {
          this.errorMessage = 'Wrong password, please enter again!';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 50px;
  }
  input {
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
  }
  button {
    padding: 10px 15px;
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  