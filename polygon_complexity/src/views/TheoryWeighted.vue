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
              The weighted model is widely used in shape analysis research. 
              It quantifies the complexity of polygons by combining different properties with varying weights. 
              Due to the diversity in the selection of properties, the weighted model can be flexibly applied to reflect different types of complexity.
            </p>
            <p v-html="renderedInlineFormula(`In our system, we use the polygon complexity calculation method proposed by Thomas Brinkhoff et al. 
            It based on three parameters: Frequency of vibration ($freq$), Amplitude of vibration ($ampl$), and Deviation from Convex Hull ($conv$). 
            By combining these three parameters, the complexity of a polygon compl can be defined as:`)">
            </p>
            <p v-html="renderedBlockFormula(`C = 0.8 \\cdot ampl\\cdot freq+0.2\\cdot conv`)"></p>
            <h2>Frequency of vibration</h2>
            <p>
              Frequency of vibration describes the local variations of the polygon’s boundary, indicating the degree of concavity and convexity. It can be defined as:
            </p>
            <p v-html="renderedBlockFormula(`freq = 16(notches_{norm}-0.5)^4-8(notches_{norm}-0.5)^2+1`)">
            </p>
            <p v-html="renderedInlineFormula(`Where $notches_{norm}$ refers to the normalized number of notches, 
            representing the non-convex parts of a polygon. A $notches_{norm}$ value close to 0 or 1 indicates a smoother boundary, 
            whereas a value close to 0.5 suggests more significant variations along the boundary. It can be defined as:`)">
            </p>
            <p v-html="renderedBlockFormula(`notches_{norm} = \\frac{notches}{verticies-3}`)">
            </p>
            <p v-html="renderedInlineFormula(`Where $notches$ is the number of notches and $vertices$ is the number of vertices of polygon.`)">
            </p>
            <h2>Amplitude of vibration</h2>
            <p>Amplitude of vibration refers to the extent to which the polygon’s boundary extends relative to its convex hull, 
              indicating the increase in boundary length compared to the simplest convex hull boundary. It defined as:
            </p>
            <p v-html="renderedBlockFormula(`ampl = \\frac{boundary(pol)-boundary(convexhull(pol))}{boundary(pol)}`)">
            </p>
            <p v-html="renderedInlineFormula(`Where $boundary(pol)$ the perimeter of the polygon, $boundary(convexhull(pol))$ is the perimeter of the polygon's convex hull.`)">       
            </p>
            <h2>Deviation from the convex hull</h2>
            <p>
              Deviation from the convex hull describes the overall shape of the polygon, quantified by the difference between the area of the polygon and the area of its convex hull. It defined as:              
            </p>
            <p v-html="renderedBlockFormula(`conv = \\frac{area(convexhull(pol))-area(pol)}{area(convexhull(pol))}`)"></p>
            <p v-html="renderedInlineFormula(`Similar to the definition of ampl, $area(convexhull(pol))$ is the area of the polygon's convex hull, $area(pol)$ is the area of the polygon.`)">
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
import katex from "katex";
import "katex/dist/katex.min.css";

export default {
name: "TheroyWeighted",

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
