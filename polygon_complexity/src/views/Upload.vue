<template>
  <div>
    <h2>Please upload a image file(.jpg, .png, .gif)</h2>
    <input type="file" @change="handleFileUpload" multiple/> 
    <button @click="uploadFile" :disabled="selectedFiles.length ===0">Yes</button>

    <ul>
      <li v-for="(fileName, index) in fileNames" :key="index">{{ fileName }}</li>
    </ul>

    <DataVisualization :data="responseData" />
  </div>
</template>

<script>
import axios from 'axios';
import DataVisualization from '../components/DataVisualization.vue';

export default {
  name: 'UploadFile',
  data() {
    return {
      selectedFiles: [], 
      responseData: null, 
      fileNames:[],
    };
  },
  components: { 
    DataVisualization,
  },
  methods: {
    handleFileUpload(event) {
      const newFiles = Array.from(event.target.files);
      this.selectedFiles = [...this.selectedFiles, ...newFiles];

      const files = event.target.files;
      //this.fileNames = [];
      for (let i = 0; i < files.length; i++) {
        this.fileNames.push(files[i].name);
      }
    },

    async uploadFile() {
      console.log(this.selectedFiles.length);
      if (this.selectedFiles.length ==0) return;

      const formData = new FormData();
      formData.append('type', 'image');

       this.selectedFiles.forEach((file, index) => {
        formData.append(`file${index}`, file);  // 用 file0, file1, ... 命名每个文件
      }); 

      try {
        const response = await axios.post('http://localhost:5000/api/complexity', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          },
        });

        const rawData = response.data.data;
        console.log(rawData);
  
        // 将后端返回的对象转换为数组格式
        const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
        });

        // 将转换后的数据赋值给 this.responseData，以便传递给 DataVisualization 组件
        this.responseData = polygonData;
  
        console.log(this.responseData);

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
