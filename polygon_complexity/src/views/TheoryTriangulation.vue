<template>
  <div class="container">

    <el-container>
      <Sidebar1 />

      <el-container class="main-content" direction="vertical">
        <PageHeader1 />
  
        <!-- Content -->
        <el-main class="content">
          <div class="introduction">
            <p v-html="renderedInlineFormula(`Polygon Triangulation involves dividing a polygon into triangles such that the union of these triangles covers 
            the entire polygon without overlapping parts. Triangulation is widely applied in diverse fields such as calculating areas and volumes of polygons or complex shapes, 
            collision detection, physical simulations, and graphics rendering. Godfried Toussaint proposed that triangulation can be used as a measure of polygon complexity. 
            For a given polygon $P$, after triangulation, $t_0$ represents the number of triangles in the output triangulation that do not share any edges with the original polygon. 
            This parameter $t_0$ can intuitively measuring the complexity`)"></p>
            <p v-html="renderedInlineFormula(`For instance, in Figure 1, the triangles are labeled accordingly to how many sides they share with the sides of the polygon. 
            We see that there two triangles labeled zero, thus the polygon illustrated has $t_0 = 2$. `)"></p>
            <figure class="image-with-caption">
              <span><img src="../assets/triangulation1.png"></span>
              <figcaption>Figure 1</figcaption>
            </figure>
            <p v-html="renderedInlineFormula(`However, for the same polygon, sometimes there will be multiple different triangulations, so $t_0$ will also be different, 
            as the Figure 2 illustrates.  `)"></p>
            <p v-html="renderedInlineFormula(`In our system, we use Fortune algorithm to get Constrained Delaunay Triangulation (CDT) of polygon. 
            Delaunay triangulation generates triangles with relatively uniform angles, helping to avoid the formation of elongated or narrow triangles.
             Figure 3 illustrates a triangulation that satisfies the Constrained Delaunay Triangulation (CDT), where $t_0=2.$  `)"></p>
          </div>
          <figure class="image-with-caption">
              <span><img src="../assets/triangulation2.png"></span>
              <figcaption>Figure 2</figcaption>
            </figure>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import router from '../router';
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader1 from '../components/PageHeader1.vue';
import katex from "katex";
import "katex/dist/katex.min.css";

export default {
name: "TheoryTriangulation",

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
  width: 500px; /* 根据需求调整大小 */
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
