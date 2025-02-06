<template>
  <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 />
        <div class = 'main-content-wrapper'>
          <div class="content-wrapper">
          <div class="text-container">
          <p><strong>FileName: </strong>{{ fileName }}</p>
          <p> <strong>Method: </strong>Boundary</p>
          <p><strong>Complexity: </strong>{{ complexity }}</p>
        </div>
        <img :src="this.url" class="imageclass">
        </div>
        <el-divider/>
        <el-table :data="[details]" border>
          <el-table-column prop="size_length" label="Length"></el-table-column>
          <el-table-column prop="size_width" label="Width"></el-table-column>
          <el-table-column prop="total_changes" label="Total changes"></el-table-column>
          <el-table-column prop="max_changes" label="Max changes"></el-table-column>
          <el-table-column prop="complexity" label="Complexity"></el-table-column>
        </el-table>
        </div>
      </el-container>
    </el-container>
  </div>
    <!--<div>
      <h1>Boundary details</h1>
      <p><strong>filename:</strong> {{ fileName }}</p>
      <p><strong>complexity:</strong> {{ complexity }}</p>
      <div>{{ details }}</div>
      <table border="1">
        <thead>
          <tr>
            <th>Length</th>
            <th>Width</th>
            <th>Total changes</th>
            <th>Max changes</th>
            <th>Complexity</th>
          </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ details.size_length }}</td>
                <td>{{ details.size_width }}</td>
                <td>{{ details.total_changes }}</td>
                <td>{{ details.max_changes }}</td>
                <td>{{ details.complexity }}</td>
            </tr>
        </tbody>
      </table>
    </div>-->
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import Sidebar1 from "../components/Sidebar1.vue";
  import PageHeader2 from "../components/PageHeader2.vue";
  import {store} from '../store/store';
  import preload1Img from '../assets/preload_images/file6.jpg';
  import preload2Img from '../assets/preload_images/file17.jpg';

  export default {

    components:{
      Sidebar1,
      PageHeader2,
    },

    data(){
      return{
        url:null,
      }
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
        console.log(this.url);
        return this.$route.params.fileName;
      },

      complexity(){
        return this.$route.query.complexity;
      },

      details(){
        return this.$store.getters.getDetails;
      },

      ...mapGetters(["getDetails"]), 
    },
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
</style>

  