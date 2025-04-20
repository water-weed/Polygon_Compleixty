<template>
    <div class="container">
  
      <el-container>
        <Sidebar1 />
        <el-container class="main-content">
          <PageHeader2 />
          <el-main class="content">
            <div class = "content-wrapper">
              <!-- description word-->
              <h1>Welcome to polygon complexity system!</h1>
              <p>The following table shows some preload images as examples, you can choose a function to get started!</p>

              <!--functionality-->
              <div class="card-container">
                <el-card  class="nav-card" @click="goTo('Select')">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'list-check']" /></span>
                      <span class="icon-text">Select</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                    <!--
                    <div class="card-right">
                      <span class = "description"> Select polygons from a preloaded list!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>-->
                  </div>
                </el-card>

                <el-card class="nav-card" @click="goTo('Upload')">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'upload']" /></span>
                      <span class="icon-text">Upload</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                    <!--
                    <div class="card-right">
                      <span class = "description"> Upload some polygon image files!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>-->
                  </div>
                </el-card>

                <el-card  class="nav-card" @click="goTo('Draw')">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'pencil']" /></span>
                      <span class="icon-text">Draw</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                    <!--
                    <div class="card-right">
                      <span class = "description"> Draw some polygons by yourself!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>-->
                  </div>
                </el-card>
                
                <el-card class="nav-card" @click="handleExport">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'file-export']" /></span>
                      <span class="icon-text">Download</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                    <!--
                    <div  class="card-right">
                      <span class = "description"> Download the complexity table!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>-->
                  </div>
                </el-card>
              </div>
            </div>
            <!--Data table-->
            <DataTable :data="store.polygonResult" :urls="store.polygonUrl" @file-generated = "updateExcelUrl"/>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>
    
  <script>
  import Sidebar1 from '../components/Sidebar1.vue';
  import PageHeader2 from '../components/PageHeader2.vue';
  import DataTable from '../components/DataTable.vue';
  import {store} from '../store/store';
  
  export default {
    name: "System",

    data(){
      return{
        store,
        excelUrl:null,
      }
    },

    components: {
      Sidebar1,
      PageHeader2,
      DataTable,
    },

    methods: {
    goTo(routeName) {
      this.$router.push({ name: routeName }); // Vue Router route jump
    },

    updateExcelUrl(url) {
      this.excelUrl = url; // update father component fileUrl
      //console.log("Received fileUrl from DataTable:", url);
    },

    handleExport() {
      if (!this.excelUrl) return;

      const link = document.createElement("a");
      link.href = this.excelUrl;
      link.setAttribute("download", "exported_data.xlsx");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
  },
  };
  </script>
    
  <style scoped>
  /*page layout style*/
  .container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
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
    min-height: 950px;
  }

  .content-wrapper {
  max-width: 97%; 
  /*height: 900px;*/ 
  overflow: auto; 
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding-bottom: 50px;
  margin-bottom: 40px; 
}
  
  .introduction {
    max-width: 95%;
    margin: auto;
    text-align: left;
  }
  
 
  /*title style*/
  h1 {
    margin-bottom: 10px;
    color: #00443c;
    text-align: left;
    padding-left: 40px;
  }
  
  /*word style*/
  p {
    font-size: 25px;
    line-height: 1.6;
    color: rgb(128, 68, 0);
    text-align: left;
    padding-left: 40px;
  }

  /*functionality card style*/
  .card-container {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  padding-left: 40px;
}

.nav-card {
  width: 20%;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  position: relative;
}

.nav-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-left {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 40px;
  font-weight: bold;
}

.card-right {
  display: flex;
  align-items: left;
  gap: 6px;
  font-size: 20px;
}

/*functionality icon*/
.icon1 {
  font-size: 30px;
  color: #00443c;
}

/*arrow*/
.icon2{
  font-size: 35px;
  color:#00443c;
  margin-left: auto;
}

/*text*/
.icon-text{
  color: #00443c;
  font-size: 28px;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.description {
  color: #00443c;
  text-align: left;
}
  </style>
    