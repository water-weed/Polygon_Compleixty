<template>
  <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 />
        <div class = 'main-content-wrapper'>
          <!--file information + image-->
          <div class="content-wrapper">
          <div class="text-container">
          <p><strong>FileName: </strong>{{ fileName }}</p>
          <p> <strong>Method: </strong>Boundary</p>
          <p><strong>Complexity: </strong>{{ complexity }}</p>
        </div>
        <!--image-->
        <img :src="this.url" class="imageclass">
        </div>
        <el-divider/>
        <!--boundary data-->
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
  </template>
  
  <script>
  import { mapGetters } from "vuex";
  import Sidebar1 from "../components/Sidebar1.vue";
  import PageHeader2 from "../components/PageHeader2.vue";
  import {store} from '../store/store';
  import preload1Img from '../assets/preload_images/preload1.jpg';
  import preload2Img from '../assets/preload_images/preload2.jpg';

  export default {

    components:{
      Sidebar1,
      PageHeader2,
    },

    data(){
      return{
        url:null, //image url
      }
    },

    computed:{
      //get file name 
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

      //get complexity
      complexity(){
        return this.$route.query.complexity;
      },
      
      //get details
      details(){
        return this.$store.getters.getDetails;
      },

      ...mapGetters(["getDetails"]), 
    },
  };
  </script>

<style scoped>
/*table style */
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

/*page layout */
.container {
  display: flex;
  align-items: center; 
  justify-content: flex-start; 
  gap: 20px; 
  height: 100vh;
}

.text-container {
  text-align: left; 
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

/* main content */
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

/*image style */
.imageclass{
  width: 150px;
  display: flex;
  margin-left: 40px;
}

/*file information + image layout */
.content-wrapper {
  display: flex;
  align-items: center; 
  justify-content: flex-start; 
  gap: 20px; 
  margin-bottom: 20px; 
  margin-top:20px;
  width: 95%;
}

/*table word and position style*/
:deep(.el-table) {
  font-size: 14px; 
  width: 95% !important; 
  margin: 0 auto;
}


/* table header word color */
:deep(.el-table__header-wrapper th) {
  color: #a5c2be; 
}

/* table content word color */
:deep(.el-table__body-wrapper td) {
  color: rgb(100, 53, 0); 
}

.main-content-wrapper{
  max-width: 95%;
}
</style>

  