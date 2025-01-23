<template>
  <div class="container">
    <el-container>
      <Sidebar2 />
      <el-container class="main-content">
        <PageHeader1 />

        <el-main class="content">
          <input type="file" @change="handleFileUpload" multiple/> 
    <button @click="uploadFile" :disabled="selectedFiles.length ===0">Yes</button>

    <ul>
      <li v-for="(fileName, index) in fileNames" :key="index">{{ fileName }}</li>
    </ul>

    <DataTable :data="responseData" :urls="fileUrls"/>
    <!--<ComplexityTable :data="responseData" :urls="fileUrls"/>-->
        </el-main>
      </el-container>
    </el-container>
  </div>>
</template>

<script>
import axios from 'axios';
import DataVisualization from '../components/DataVisualization.vue';
import Sidebar2 from '../components/Sidebar2.vue';
import PageHeader1 from '../components/PageHeader1.vue';
import DataTable from '../components/DataTable.vue';

export default {
  name: 'UploadFile',
  data() {
    return {
      selectedFiles: [], 
      responseData: null, 
      fileNames:[],
      fileUrls:{}
    };
  },
  components: { 
    DataVisualization,
    Sidebar2,
    PageHeader1,
    DataTable,
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
        this.fileUrls[`file${index}`]= URL.createObjectURL(file);
      }); 

      console.log(this.fileUrls)

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

.el-container {
  height: 100%;
}

.main-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  width: 100%;
  background-color: #f5f5f5;
}

/* 主内容 */
.content {
  padding: 20px;
  text-align: center;
  background-color: #f5f5f5;
  flex-grow: 1;
  width: 100%;
}

button{
  border: 2px solid rgb(128, 68, 0);
  color: rgb(128, 68, 0);
}

button:hover{
  background-color: #fdca6b;
  color: white;
  border: none;
}

button:active{
  background-color: #fdca6b;
  color: #f9f9f9;
  border: none;
}
</style>
