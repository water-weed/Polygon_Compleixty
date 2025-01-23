<template>
  <div class="container">

    <el-container>
      <Sidebar1 />

      <el-container class="main-content" direction="vertical">
        <PageHeader1 />
  
        <!-- Content -->
        <el-main class="content">
          <div class="introduction">
            <h2>Background</h2>
            <p>
              Quantifying shape complexity has a long history of research in the fields of computer vision, manufacturing, geographic information systems
              (GIS), and human perception. Researchers have employed various theories and proposed many notions of shape complexity from different perspectives,
              all aiming to find a definition of shape complexity that is consistent with human intuition and applicable to their fields of research.
            </p>
            <el-divider />
            <h2>Project Description</h2>
            <p>
              Polygons are fundamental shapes and often are the result of sampling in most shape studies. Therefore, in this thesis, we explore different definitions
              of polygon complexity and categorize them into six groups based on the methodology: downsampling measures, geometric measures, information 
              theory-based measures, machine learning measures, skeleton-based measures, and weighted measures, according to the underlying theory or features of the 
              definition.
            </p>
            <p>
              We design a web-based system to demonstrate the main existing measures for quantifying polygon complexity. The system reproduces 
              more than ten measures summarized in the thesis and provides data visualization of the calculation results. 
              Additionally, the system offers three methods for inputting polygons: selecting existing polygons, uploading polygon 
              images, and drawing polygons directly on the web page, giving users greater freedom. We hope this system can help users understand these methods 
              and their differences more intuitively and conveniently.
            </p>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
  
<script>
import router from '../router';
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader1 from '../components/PageHeader1.vue';

export default {
  name: "Home1",

  components: {
    Sidebar1,
    PageHeader1,
  },
};
</script>
  
<style scoped>
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

/* 主内容 */
.content {
  padding: 20px;
  text-align: center;
  background-color: #f5f5f5;
  flex-grow: 1;
  width: 100%;
}

.introduction {
  max-width: 95%;
  margin: auto;
  text-align: left;
}

/* ✅ 标题样式 */
h2, h3 {
  margin-bottom: 10px;
  color: #00443c;
}

/* ✅ 文字样式 */
p {
  font-size: 22px;
  line-height: 1.6;
  color: rgb(128, 68, 0);
}
</style>
  