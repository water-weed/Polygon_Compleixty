<template>
    <div class="container">

      <el-container>
      <Sidebar1 />

      <el-container class="main-content" direction="vertical">
        <PageHeader1 />
  
        <!-- Content -->
        <el-main class="content">
          <el-main>
      <el-row :gutter="30">
        <!-- method 1: select-->
        <el-col :span="24" class="feature-col">
          <el-card class="feature-card">
            <el-row align="middle">
              <!-- left:text -->
              <el-col :span="12">
                <div class="feature-text">
                  <h3>Select </h3>
                  <p>Select and upload from an existing list of polygons.</p>
                </div>
              </el-col>

              <!-- right:image -->
              <el-col :span="12" >
                <img src="../assets/select.gif" alt="Select Polygons" class="feature-image" />
              </el-col>
            </el-row>
          </el-card>
        </el-col>

        <!-- method 2: upload -->
        <el-col :span="24" class="feature-col">
          <el-card class="feature-card">
            <el-row align="middle">
              <!-- left:image -->
              <el-col :span="12">
                <img src="../assets/upload.gif" alt="Upload Polygons" class="feature-image" />
              </el-col>

              <!--right:text-->
              <el-col :span="12">
                <div class="feature-text">
                  <h3>Upload</h3>
                  <p>Directly upload an image of a polygon.</p>
                </div>
              </el-col>          
            </el-row>
          </el-card>
        </el-col>

        <!-- method 3: draw -->
        <el-col :span="24" class="feature-col">
          <el-card class="feature-card">
            <el-row align="middle">
              <!-- left：text -->
              <el-col :span="12">
                <div class="feature-text">
                  <h3>Draw </h3>
                  <p>Draw a polygon on the canvas.</p>
                </div>
              </el-col>

              <!-- right：image -->
              <el-col :span="12">
                <img src="../assets/draw.gif" alt="Draw Polygons" class="feature-image" />
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
        </el-main>
      </el-container>
    </el-container>
    </div>
  </template>
  
<script>
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader1 from '../components/PageHeader1.vue';

export default {
  name: "SystemDescription",

  components: {
    Sidebar1,
    PageHeader1,
  },
};
</script>
  
<style scoped>
/*page layout style*/
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
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

.section-title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

/*el-card style */
.feature-card {
  background-color: white;
  padding: 20px;
}

/* text style*/
.feature-text {
  text-align: left;
  padding-left: 20px;
}

.feature-text h3 {
  font-size: 35px;
  color: #00443c;
}

.feature-text p {
  font-size: 25px;
  color: rgb(128, 68, 0);
  line-height: 1.6;
}

/* image style */
.feature-image {
  width: 100%;
  max-width: 800px;
  display: block;
  margin: auto;
}

.feature-col {
  margin-bottom: 35px;
}
</style>
  