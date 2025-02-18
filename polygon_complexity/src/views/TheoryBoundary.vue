<template>
  <div class="container">

    <el-container>
      <Sidebar1 />

      <el-container class="main-content" direction="vertical">
        <PageHeader1 />
  
        <!-- Content -->
        <el-main class="content">
          <div class="introduction">
            <p>
              Length is one of the most basic properties of polygons, so it is not difficult to think of using the boundary length to measure the complexity of polygons. 
              Looking at the example of Figure1 we can see that the length of the boundary of shape 1 is much longer than shape 2 and at the same time shape 1 looks more complex than shape 2.
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/preload_images/file1.jpg"></span>
              <span><img src="../assets/preload_images/file12.jpg"></span>
              <figcaption>Figure 1</figcaption>
            </figure>
            <p v-html="renderedInlineFormula(`Michiharu Niimi et al. Proposed that the four-connectivity neighborhood method can be used to measure the boundary length of a polygon.
             This method represents the boundary length $k$ by calculating the length of the black and white boundary in the image, which is the number of color changes in the rows 
             and columns of the image. To further understand this, in a black-and-white image, pixel transitions between black and white occur along the polygon's boundary. 
             The greater the number of such transitions, the longer the polygon's boundary .For example, using this method, the boundary 
             length of the Figure 2 is 39. For an image of size $2^m \\times 2^m$ pixels, the minimum boundary length is 0, and the maximum boundary length is $2 \\times 2^m \\times (2m − 1)$. 
             As mentioned before, we need to normalize the boundary lengths to the same scale for comparison, so the complexity $C_{boundary}$ is defined as:`)"></p>
             <p v-html="renderedBlockFormula(`C_{boundary}=\\frac{k}{2\\times2^m\\times(2^m-1)}`)"></p>
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
import { computed } from 'vue';
import katex from "katex";
import "katex/dist/katex.min.css";


export default {
name: "TheoryBoundary",



components: {
  Sidebar1,
  PageHeader1,
},

methods: {
  renderedInlineFormula(inlineText) {
      return inlineText.replace(/\$(.*?)\$/g, (match, formula) =>
        katex.renderToString(formula, { throwOnError: false, displayMode: false })
      );
    },

    renderedBlockFormula(blockFormula) {
      return katex.renderToString(blockFormula, { throwOnError: false, displayMode: true });
    }
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Edu+TAS+Beginner:wght@400..700&display=swap');
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

/* 主内容 */
.content {
  padding: 20px;
  text-align: center;
  background-color: #f5f5f5;
  flex-grow: 1;
  width: 100%;
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
  width: 200px; /* 根据需求调整大小 */
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
</style>
