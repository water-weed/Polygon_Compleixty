<template>
    <div class="container">
  
      <el-container>
        <Sidebar1 />
        <el-container class="main-content">
          <PageHeader2 />
          <el-main class="content">
            <div class = "content-wrapper">
              <!-- 说明文字 -->
              <h1>Welcome to polygon complexity system!</h1>
              <p>The following table shows some preload images as examples, you can choose a function to get started!</p>

              <div class="card-container">
                <el-card  class="nav-card" @click="goTo('Select')">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'list-check']" /></span>
                      <span class="icon-text">Select</span>
                    </div>
                    <div class="card-right">
                      <span class = "description"> Select polygons from a preloaded list!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                  </div>
                </el-card>

                <el-card class="nav-card" @click="goTo('Upload')">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'upload']" /></span>
                      <span class="icon-text">Upload</span>
                    </div>
                    <div class="card-right">
                      <span class = "description"> Upload some polygon image files!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                  </div>
                </el-card>

                <el-card  class="nav-card" @click="goTo('Draw')">
                  <div class="card-content">
                    <div class="card-left">
                      <span class="icon1"><font-awesome-icon :icon="['fas', 'pencil']" /></span>
                      <span class="icon-text">Draw</span>
                    </div>
                    <div class="card-right">
                      <span class = "description"> Draw some polygons by yourself!</span>
                      <span class = 'icon2'><font-awesome-icon :icon="['far', 'circle-right']" /></span>
                    </div>
                  </div>
                </el-card>
              </div>
            </div>
            <DataTable/>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>
    
  <script>
  import Sidebar1 from '../components/Sidebar1.vue';
  import PageHeader2 from '../components/PageHeader2.vue';
  import DataTable from '../components/DataTable.vue';
  
  export default {
    name: "System",
  
    components: {
      Sidebar1,
      PageHeader2,
      DataTable,
    },

    methods: {
    goTo(routeName) {
      this.$router.push({ name: routeName }); // Vue Router 路由跳转
    },
  },
  };
  </script>
    
  <style scoped>
  .container {
    display: flex;
    flex-direction: column;
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

  .content-wrapper {
  max-width: 97%; /* 限制宽度 */
  height: 900px; /* 固定高度 */
  overflow: auto; /* 让内容滚动 */
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; /* 与 DataTable 分开 */
}
  
  .introduction {
    max-width: 95%;
    margin: auto;
    text-align: left;
  }
  
 
  h1 {
    margin-bottom: 10px;
    color: #00443c;
    text-align: left;
    padding-left: 40px;
  }
  
  p {
    font-size: 25px;
    line-height: 1.6;
    color: rgb(128, 68, 0);
    text-align: left;
    padding-left: 40px;
  }

  .card-container {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  padding-left: 40px;
}

.nav-card {
  width: 400px;
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
  font-size: 20px;
  font-weight: bold;
}

.card-right {
  display: flex;
  align-items: left;
  gap: 6px;
  font-size: 20px;
}

.icon1 {
  font-size: 30px;
  color: #00443c;
}

.icon2{
  font-size: 35px;
  color:#00443c;
  margin-left: auto;
}

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
    