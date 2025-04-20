<template>
  <div class="container">
    <el-container>
      <Sidebar1 />

      <!--main content-->
      <el-container class="main-content">
        <PageHeader2 />

        <el-main class="content">
          <div class="content-wrapper">
            <!--upload-->
            <el-upload
              ref="uploadRef"
              action=""
              :auto-upload="false"
              :on-change="handleFileUpload"
              :multiple="true"
              :file-list="selectedFiles"
              accept="image/*"
              list-type="picture-card"
            >
            <el-icon><Plus /></el-icon>
            </el-upload>

            <!--button-->
            <div class="button-container">
               <el-button  @click="cancelFiles">
                Cancel
              </el-button>
              <el-button  @click="uploadFile" :disabled="selectedFiles.length === 0">
                Ok
              </el-button>
            </div>        
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios';
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader2 from '../components/PageHeader2.vue';
import DataTable from '../components/DataTable.vue';
import { Plus } from "@element-plus/icons-vue";
import {store} from '../store/store';


export default {
  name: 'UploadFile',
  data() {
    return {
      selectedFiles: [], //user selected files
      responseData: null, //response data
      fileNames:[],
      fileUrls:{},//filename ->url
    };
  },
  components: { 
    Sidebar1,
    PageHeader2,
    DataTable,
    Plus,
  },


  methods: {
    //update file list after file selection
    handleFileUpload(file, fileList) {
      //const newFiles = Array.from(event.target.files);
      //this.selectedFiles = [...this.selectedFiles, ...newFiles];

      //const files = event.target.files;
      //this.fileNames = [];
      //for (let i = 0; i < files.length; i++) {
        //this.fileNames.push(files[i].name);
      //}
      this.selectedFiles = fileList;
      //this.fileUrls = this.selectedFiles.reduce((acc, file, index) => {
        //acc[`file${index}`] = URL.createObjectURL(file.raw); 
        //acc[`file${store.n}`] = URL.createObjectURL(file.raw);
        //this.fileNames.push(`file${store.n}`);
        //store.n ++;
        //return acc;
        //}, {});
      //console.log(this.fileUrls);
    },

    //cancel upload, clear all data
    cancelFiles(){
      this.$refs.uploadRef.clearFiles();
      this.selectedFiles= [];
      this.fileUrls={};
      this.$router.push({ name: 'System' });
    },

    //upload file and handle response data
    async uploadFile() {
      //console.log(this.selectedFiles.length);
      if (this.selectedFiles.length ==0) return;

      const formData = new FormData();
      //console.log(formData);
      formData.append('type', 'image');
      //console.log(this.selectedFiles);

      //traverse the file list, append the formdata and generate the url
       this.selectedFiles.forEach((file, index) => {
        formData.append(`file${store.n}`, file.raw);  // name each file file0, file1
        this.fileUrls[`file${store.n}`]= URL.createObjectURL(file.raw);
        store.n ++;
      }); 
      /*formData.forEach((value, key) => {
        console.log(key, value);
      });*/

      try {
        const response = await axios.post('http://localhost:5000/api/complexity', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          },
        });

        const rawData = response.data.data;
        console.log(rawData);
  
        // convert the object returned by the backend into an array format
        const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
        });

        // assign the converted dat to this response Data
        this.responseData = polygonData;
        store.polygonResult = [...store.polygonResult, ...this.responseData];
        store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
      //console.log(Urls);
        /*store.polygonResult = [...store.polygonResult, ...this.responseData.slice(store.polygonResult.length)];
        //console.log(store.polygonResult);
        store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
        this.responseData.forEach((polygon, index)=>{
          const contains = store.polygonResult.some(item => lodash.isEqual(item, polygon));
          console.log(contains);
          if(!contains){
            let storeIndex = store.polygonResult.length;
            console.log(storeIndex);
            const newkey = `file${storeIndex}`;
            const oldkey = Object.keys(polygon)[0];

            const storeAddUrl = {}
            storeAddUrl[`file${storeIndex}`] = this.fileUrls[Object.keys(polygon)];
            store.polygonUrl = {...store.polygonUrl,...storeAddUrl};
            console.log(store.polygonUrl);

            polygon[newkey] = polygon[oldkey];
            delete polygon[oldkey];
            console.log(polygon);
            store.polygonResult.push(polygon);*/
            
            //console.log(store.polygonResult);
            //claer all data
            this.$refs.uploadRef.clearFiles();
            this.selectedFiles= [];
            this.fileUrls={};
            this.$router.push({ name: 'System' });
        //console.log(this.responseData);

      } catch (error) {
        console.error('Failure', error);
      }
    },
  },
  setup() {
    return { Plus };
  },
};
</script>

<style scoped>
/*page layout style*/
 .content-wrapper {
  max-width: 97%; 
  overflow: auto; 
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /*margin-bottom: 20px;*/ 
  padding-bottom: 50px;
}

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
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* main content */
.content {
  padding: 20px;
  text-align: center;
  background-color: #f5f5f5;
  flex-grow: 1;
  width: 100%;
}

/*button style*/
.el-button{
  border: 2px solid rgb(128, 68, 0);
  color: rgb(128, 68, 0);
}

.el-button:hover{
  background-color: #fdca6b;
  color: white;
  border: none;
}

.el-button:active{
  background-color: #fdca6b;
  color: #f9f9f9;
  border: none;
}

  .image-preview {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.preview-item img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
  border: 1px solid #ddd;
  padding: 5px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px; 
  margin-top: 40px;
}

/*upload window style*/
::v-deep(.el-upload-list--picture-card .el-upload) {
  width: 300px !important;
  height: 300px !important;
}

::v-deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 300px !important;
  height: 300px !important;
}

</style>