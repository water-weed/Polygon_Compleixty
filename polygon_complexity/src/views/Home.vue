<!-- src/views/Home.vue -->
<template>
    <div class="home">
      <h1>Welcome to polygon complexity system</h1>
      <p>Please choose functions:</p>
      <ul>
        <li><router-link to="/Select">Select</router-link></li>
        <li><router-link to="/Upload">Upload</router-link></li>
        <li><router-link to="/Draw">Draw</router-link></li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home'
  };
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    margin-top: 50px;
  }
  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 10px 0;
  }
  a {
    text-decoration: none;
    color: #42b983;
    font-size: 1.2em;
  }
  a:hover {
    text-decoration: underline;
  }
  </style>