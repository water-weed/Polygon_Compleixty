<!-- src/views/Select.vue -->
<template>
  <div class="container">
    <el-container>
      <Sidebar2 />
      <el-container class="main-content">
        <PageHeader1 />

        <el-main class="content">
    <!--<DataVisualization :data="responseData" :urls="fileUrls"/>-->
    <SelectImage @upload-success="handleUploadSuccess" />
    <DataTable :data="responseData" :urls="fileUrls"/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import DataVisualization from '../components/DataVisualization.vue';
import SelectImage from '../components/SelectImage.vue';
import Sidebar2 from '../components/Sidebar2.vue';
import PageHeader1 from '../components/PageHeader1.vue';
import DataTable from '../components/DataTable.vue';

export default {
  name: 'Select',
  components: {
    SelectImage,  
    DataVisualization,
    Sidebar2,
    PageHeader1,
    DataTable,
  },
  data() {
    return {
      responseData: null, 
      fileUrls:{}
    };
  },
  methods: {
    handleUploadSuccess(data,Urls) {
      this.responseData = data;
      this.fileUrls = Urls;
      //console.log(Urls);
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.response-data {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #fdca6b;;
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
