<template>
  <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 />

        <el-main class="content">
          <div class="content-wrapper">
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
import DataVisualization from '../components/DataVisualization.vue';
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader2 from '../components/PageHeader2.vue';
import DataTable from '../components/DataTable.vue';
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import {store} from '../store/store';
import lodash from "lodash";


export default {
  name: 'UploadFile',
  data() {
    return {
      selectedFiles: [], 
      responseData: null, 
      fileNames:[],
      fileUrls:{},
    };
  },
  components: { 
    DataVisualization,
    Sidebar1,
    PageHeader2,
    DataTable,
    Plus,
  },


  methods: {
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
        //acc[`file${index}`] = URL.createObjectURL(file.raw); // 生成本地预览 URL
        //acc[`file${store.n}`] = URL.createObjectURL(file.raw);
        //this.fileNames.push(`file${store.n}`);
        //store.n ++;
        //return acc;
        //}, {});
      //console.log(this.fileUrls);
    },

    cancelFiles(){
      this.$refs.uploadRef.clearFiles();
      this.selectedFiles= [];
      this.fileUrls={};
      this.$router.push({ name: 'System' });
    },

    async uploadFile() {
      //console.log(this.selectedFiles.length);
      if (this.selectedFiles.length ==0) return;

      const formData = new FormData();
      //console.log(formData);
      formData.append('type', 'image');
      //console.log(this.selectedFiles);

       this.selectedFiles.forEach((file, index) => {
        formData.append(`file${store.n}`, file.raw);  // 用 file0, file1, ... 命名每个文件
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
  
        // 将后端返回的对象转换为数组格式
        const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
        });

        // 将转换后的数据赋值给 this.responseData，以便传递给 DataVisualization 组件
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
 .content-wrapper {
  max-width: 97%; /* 限制宽度 */
  overflow: auto; /* 让内容滚动 */
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /*margin-bottom: 20px;*/ /* 与 DataTable 分开 */
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

/* 主内容 */
.content {
  padding: 20px;
  text-align: center;
  background-color: #f5f5f5;
  flex-grow: 1;
  width: 100%;
}

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
  justify-content: center; /* 居中对齐 */
  gap: 20px; /* 设置按钮间距 */
  margin-top: 40px;
}

::v-deep(.el-upload-list--picture-card .el-upload) {
  width: 300px !important;
  height: 300px !important;
}

::v-deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 300px !important;
  height: 300px !important;
}

</style>