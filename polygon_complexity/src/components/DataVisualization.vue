<<<<<<< HEAD
<template>
    <div v-if="responseData" class="response-data">
      <p>{{ responseData.message }}</p>
      <p>{{ responseData.data }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DataVisualization',
    props: {
      responseData: {
        type: Object,
        required: false, // 允许 responseData 为空
      }
    }
  };
  </script>
  
  <style scoped>
  .response-data {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #42b983;
    background-color: #f9f9f9;
  }
=======
<template>
    <div v-if="responseData" class="response-data">
      <p>{{ responseData.message }}</p>
      <p>{{ responseData.data }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DataVisualization',
    props: {
      responseData: {
        type: Object,
        required: false, // 允许 responseData 为空
      }
    }
  };
  </script>
  
  <style scoped>
  .response-data {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #42b983;
    background-color: #f9f9f9;
  }
>>>>>>> 9940b710187e10b903004c6d68852d2e6f417ace
  </style>