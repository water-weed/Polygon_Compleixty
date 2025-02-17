<template>
    <!--<div>
      <h1>Mat details</h1>
      <p><strong>filename:</strong> {{ fileName }}</p>
      <p><strong>complexity:</strong> {{ complexity }}</p>
      <div>{{ details }}</div>
      <img :src="imageUrl" alt="Base64 Image" v-if="imageUrl" />
    </div>-->

    <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 />
        <div class = 'main-content-wrapper'>
          <div class="content-wrapper">
          <div class="text-container">
          <p><strong>FileName: </strong>{{ fileName }}</p>
          <p> <strong>Method: </strong>Media axis transform(MAT)</p>
          <p><strong>Complexity: </strong>{{ complexity }}</p>
        </div>
        <img :src="this.url" class="imageclass">
        </div>
        </div>
        <el-divider/>
        <img :src="this.imageUrl" class="imageclass1">
      </el-container>
    </el-container>
  </div>  
</template>
  
<script>
import Sidebar1 from "../components/Sidebar1.vue";
import PageHeader2 from "../components/PageHeader2.vue";
import {store} from '../store/store';
import preload1Img from '../assets/preload_images/file6.jpg';
import preload2Img from '../assets/preload_images/file17.jpg';

  export default {
    data(){
      return{
        imageUrl:null,
        url:null,
      }
    },

  components:{
    Sidebar1,
    PageHeader2,
  },

    watch: {
    // 监听 details 数据的变化
    details: {
      handler(newDetails) {
        if (newDetails.img) {
          // 释放旧的 URL
          if (this.imageUrl) {
            URL.revokeObjectURL(this.imageUrl);
          }
          // 生成新的 URL
          this.imageUrl = this.createImageUrl(newDetails.img);
        }
      },
      immediate: true, // 立即执行一次，确保初始值
      deep: true, // 深度监听
    },
  },

    mounted() {
      this.imageUrl = this.createImageUrl(this.details.img);
    },
    
    computed:{
      fileName(){
        if (this.$route.params.fileName == 'preload1'){
          this.url = preload1Img;
        }
        else if(this.$route.params.fileName == 'preload2'){
          this.url = preload2Img;
        }
        else{
          console.log(store.polygonUrl);
          this.url = store.polygonUrl[this.$route.params.fileName];
        }
        //console.log(this.url);
        return this.$route.params.fileName;
      },

      complexity(){
        return this.$route.query.complexity;
      },

      details(){
        return this.$store.getters.getDetails;
      },
    },

    methods:{
      createImageUrl(base64) {
      // 将 Base64 转换为 Blob
        const byteString = atob(base64.split(",")[1]); // 去掉前缀 "data:image/png;base64,"
        const mimeString = base64.split(",")[0].split(":")[1].split(";")[0]; // 提取 MIME 类型

      // 创建 Uint8Array 存储二进制数据
        const byteArray = new Uint8Array(byteString.length);
        for (let i = 0; i < byteString.length; i++) {
          byteArray[i] = byteString.charCodeAt(i);
        }

      // 创建 Blob 对象
        const blob = new Blob([byteArray], { type: mimeString });

      // 创建动态 URL
        return URL.createObjectURL(blob);
    },
    }
  };
  </script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}
th, td {
  padding: 8px;
  border: 1px solid #ccc;
}
thead {
  background-color: #f4f4f4;
}

.container {
  display: flex;
  align-items: center; /* 让文字和图片垂直居中对齐 */
  justify-content: flex-start; /* 让内容从左向右排列 */
  gap: 20px; /* 文字和图片之间的间距 */
  height: 1020px;
}

.text-container {
  text-align: left; /* 文字左对齐 */
  margin-left: 60px;
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

p{
  font-size: 20px;
  color:#00443c;
}

.imageclass{
  width: 150px;
  display: flex;
  margin-left: 40px;
}

.content-wrapper {
  display: flex;
  align-items: center; /* 让文字和图片垂直居中 */
  justify-content: flex-start; /* 文字在左，图片在右 */
  gap: 20px; /* 控制文字和图片之间的间距 */
  margin-bottom: 20px; /* 让图片和表格之间有间隔 */
  margin-top:20px;
  width: 95%;
}

:deep(.el-table) {
  font-size: 14px; /* 设置表格字体大小 */
  width: 95% !important; /* 让 el-table 占据 95% 宽度 */
  margin: 0 auto;
}


/* 表头字体颜色 */
:deep(.el-table__header-wrapper th) {
  color: #a5c2be; /* 修改表头字体颜色 */
}

/* 表格内容字体颜色 */
:deep(.el-table__body-wrapper td) {
  color: rgb(100, 53, 0); /* 修改表格内容字体颜色 */
}

.main-content-wrapper{
  max-width: 95%;
}

.imageclass1{
  width: 50%;
  display: block;
  margin: auto;
}
</style>
  