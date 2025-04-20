<template>
    <!--<div>
      <h1>DownsamplingArea details</h1>
      <p><strong>filename:</strong> {{ fileName }}</p>
      <p><strong>complexity:</strong> {{ complexity }}</p>
      <div>{{ details }}</div>
      <img :src="imageUrl" alt="Base64 Image" v-if="imageUrl" />
      <table border="1">
        <thead>
          <tr>
            <th>Sampling rate</th>
            <th>Complexity</th>
            <th>Original occupied pixels</th>
            <th>Total occupied pixels</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="key in sampleRate" :key="key">
            <td>{{ key }}</td>
            <td>{{ details[key].complexity }}</td>
            <td>{{ details[key].original_occupied_pixels }}</td>
            <td>{{ details[key].total_occupied_pixels }}</td>
          </tr>
        </tbody>
      </table>
    </div>-->

    <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 />
        <!--information + image-->
        <div class = 'main-content-wrapper'>
          <div class="content-wrapper">
          <div class="text-container">
          <p><strong>FileName: </strong>{{ fileName }}</p>
          <p> <strong>Method: </strong>DownsamplingArea</p>
          <p><strong>Complexity: </strong>{{ complexity }}</p>
        </div>
        <!--polygon image-->
        <img :src="this.url" class="imageclass">
        </div>
        <el-divider/>
        <!--table-->
        <el-table :data="sampleRate.map(key => ({
          samplingRate: key,
          complexity: details[key]?.complexity ?? '-',
          originalOccupiedPixels: details[key]?.original_occupied_pixels ?? '-',
          totalOccupiedPixels: details[key]?.total_occupied_pixels ?? '-'
          }))" border>
          <el-table-column prop="samplingRate" label="Sampling rate"></el-table-column>
          <el-table-column prop="complexity" label="Complexity"></el-table-column>
          <el-table-column prop="originalOccupiedPixels" label="Original occupied pixels"></el-table-column>
          <el-table-column prop="totalOccupiedPixels" label="Total occupied pixels"></el-table-column>
        </el-table>
        </div>
        <el-divider/>
        <!--downsampling image-->
        <img :src="this.imgUrl" class="imageclass1">
      </el-container>
    </el-container>
  </div>
</template>
  
<script>
  import Sidebar1 from "../components/Sidebar1.vue";
  import PageHeader2 from "../components/PageHeader2.vue";
  import {store} from '../store/store';
  import preload1Img from '../assets/preload_images/preload1.jpg';
  import preload2Img from '../assets/preload_images/preload2.jpg';
  export default {
    data(){
      return{
        url:null, //original polygon image url
        imgUrl:null, // downsampling image url
      }
    },

    components:{
      Sidebar1,
      PageHeader2,
    },

    watch: {
    // monitor changes in details data
    details: {
      handler(newDetails) {
        if (newDetails.img) {
          // release old URL
          if (this.imgUrl) {
            URL.revokeObjectURL(this.imgUrl);
          }
          // generate new URL
          this.imgUrl = this.createImageUrl(newDetails.img);
        }
      },
      immediate: true, 
      deep: true, 
    },
  },

    mounted() {
      this.imgUrl = this.createImageUrl(this.details.img);
      console.log(this.imgUrl);
    },
    //async mounted() {
    //this.$nextTick(() => {
      //if (this.details.img) {
        //this.imageUrl = this.createImageUrl(this.details.img);
      //}
    //});
  //},

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
        //console.log(this.url);
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

      //get sample rate
      sampleRate(){
        const keys = Object.keys(this.details);
        return keys.filter(key => key !== "complexity" && key !== "img");
      },
    },

    methods:{
      //convert Base64 to blob URL
      createImageUrl(base64) {
      // convert Base64 to Blob
        const byteString = atob(base64.split(",")[1]); // remove prefix "data:image/png;base64,"
        const mimeString = base64.split(",")[0].split(":")[1].split(";")[0]; // extract MIME type

      // create Uint8Array to store binary data
        const byteArray = new Uint8Array(byteString.length);
        for (let i = 0; i < byteString.length; i++) {
          byteArray[i] = byteString.charCodeAt(i);
        }

      // create Blob object
        const blob = new Blob([byteArray], { type: mimeString });

      // create new URL
        const url = URL.createObjectURL(blob);
        //console.log(url);
        return url
    },
    }
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

/*polygon image style */
.imageclass{
  width: 150px;
  display: flex;
  margin-left: 40px;
}

.content-wrapper {
  display: flex;
  align-items: center; 
  justify-content: flex-start; 
  gap: 20px; 
  margin-bottom: 20px; 
  margin-top:20px;
  width: 95%;
}

/*table word color and position */
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

/*downsampling image style*/
.imageclass1{
  width: 85%;
  display: block;
  margin-left: 40px;
}
</style>