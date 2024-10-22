<template>
  <div>
    <h2>Please upload a image file(.jpg, .png, .gif)</h2>
    <input type="file" @change="handleFileUpload" /> 
    <button @click="uploadFile" :disabled="!selectedFile">Yes</button>

    <DataVisualization :responseData="responseData" />
  </div>
</template>

<script>
import axios from 'axios';
import DataVisualization from '../components/DataVisualization.vue';

export default {
  name: 'UploadFile',
  data() {
    return {
      selectedFile: null, 
      responseData: null, 
    };
  },
  components: { 
    DataVisualization,
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0]; 
    },

    async uploadFile() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append('file', this.selectedFile); 
      formData.append('type', 'image');

      try {
        const response = await axios.post('http://localhost:5000/api/complexity', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          },
        });

        this.responseData = response.data;

        console.log(response.data);
      } catch (error) {
        console.error('Failure', error);
      }
    },
  },
};
</script>

<style scoped>
.response-data {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #42b983;
  background-color: #f9f9f9;
}
</style>
