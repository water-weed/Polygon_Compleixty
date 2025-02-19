<template>
  <div class="container">

    <el-container>
      <Sidebar1 />

      <el-container class="main-content" direction="vertical">
        <PageHeader1 />
  
        <!-- Content -->
        <el-main class="content">
          <div class="introduction">
            <p>Hongjie Chen</p>
            <p>h.chen1@students.uu.nl</p>
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
name: "About",

components: {
  Sidebar1,
  PageHeader1,
},
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Edu+TAS+Beginner:wght@400..700&display=swap');
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
  height: 1050px;
}

.introduction {
  max-width: 90%;
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
  font-size: 30px;
  line-height: 1.6;
  color: rgb(128, 68, 0);
  font-family: "Edu TAS Beginner", serif;
  font-optical-sizing: auto;
}

.image-with-caption {
  display: inline-block;
  flex-direction: column;
  align-items: center; /* 水平居中 */
  justify-content: center; /* 仅在需要时垂直居中 */
  text-align: center; /* 文字居中 */
  width: 100%; /* 让其适应父级容器 */
}

.image-with-caption img {
  width: 55%; /* 根据需求调整大小 */
  height: auto;
  margin: 20px;
}

.image-with-caption figcaption {
  font-size: 25px;
  color: #666;
  margin-top: 4px;
  font-family: "Edu TAS Beginner", serif;
  font-optical-sizing: auto;
}

:deep(.katex){
  font-family: "Edu TAS Beginner", serif!important;
  font-optical-sizing: auto!important;
}

.formula-block {
  text-align: center;
  margin: 10px 10px;
}

.img1{
  width:20%!important;
}
</style>
