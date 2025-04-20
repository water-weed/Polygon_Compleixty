<!-- src/views/Select.vue -->
<template>
  <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 />

        <!--Select window-->
        <el-main class="content">
          <div class="content-wrapper">
            <SelectImage @upload-success="handleUploadSuccess" />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import SelectImage from '../components/SelectImage.vue';
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader2 from '../components/PageHeader2.vue';
import DataTable from '../components/DataTable.vue';
import {store} from '../store/store';

export default {
  name: 'Select',
  components: {
    SelectImage,  
    Sidebar1,
    PageHeader2,
    DataTable,
  },
  data() {
    return {
      responseData: null, 
      fileUrls:{}
    };
  },
  methods: {
    //operation of handling response data
    handleUploadSuccess(data,Urls) {
      this.responseData = data;
      this.fileUrls = Urls;
      store.polygonResult = [...store.polygonResult, ...this.responseData];
      store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
      //console.log(Urls);
    }
  }
};
</script>

<style scoped>
/*Page layout*/
 .content-wrapper {
  max-width: 97%; 
  height: 900px; 
  overflow: auto; 
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; 
}

.container {
  display: flex;
  flex-direction: column;
}

.response-data {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #fdca6b;
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

/* main content*/
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
