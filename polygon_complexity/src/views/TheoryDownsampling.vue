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
              Downsampling is a signal processing technique used to reduce the sampling rate of digital signals. 
              It has wide applications in audio processing, image processing, video processing, and data analysis. 
              Downsampling has multiple functions including reducing computational complexity, minimizing noise, saving storage space, facilitating feature extraction, 
              and enabling image compression. In polygon shape studies, downsampling is a prevalent method for polygon simplification techniques. 
              Such techniques are widely employed in computer graphics geographic information systems, and computer vision, such as texture mappling, 
              computer animation and video encoding, map zooming and layering, spatial data simplification and super-resolution. By selectively retaining key vertices of a polygon, 
              downsampling preserves essential shape features while reducing data volume.
            </p>
            <p>The core idea of downsampling-based measures involves comparing the original polygon with its simplified version after downsampling to calculate the original polygon’s complexity.
               Downsampling-based measures for polygon simplification mainly have two approaches: downsampling the polygon’s boundary and downsampling the polygon’s area.
            </p>
            <h2>Downsampling boundary</h2>
            <p>
              The core idea of downsampling the boundary is reducing the number of vertices to represent the polygon. This process is illustrated in Figure 1,
              where the polygon’s boundary is successively downsampled to achieve a convex polygon with decreasing vertex counts of 100, 50, 25, and 8.
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/Downsampling1.png"></span>
              <figcaption>Figure 1</figcaption>
            </figure>
            <h2>Downsampling area</h2>
            <p v-html="renderedInlineFormula(`The core idea of downsampling the area, is partitioning the polygon into progressively larger blocks to represent its coverage area. 
            This methodology is similar to the image downsampling techniques employed in image processing. We can convert the boundary curve of the polygon into an image $I$, 
            such as a 256 \\times 256 image. Subsequently, we use a grid of size $n\\times n$ to cover the image $I$. For each grid cell, we calculate the filling rate, that is, 
            the percentage of the overlap between the grid cell and the image $I$ to the total area of the grid cell. If the filling rate > 0.5, then this grid belongs to image $I$, 
            otherwise it belongs to background. As we gradually increase the grid size $n$, the number of grids in the image decreases, 
            the resolution of the downsampled polygon becomes lower, and the downsampled polygon tends to become simpler. Figure 2 depicts the $256\\times 256$ image and 
            its downsampling results for n = 2, n = 4, n = 8, and n = 16.`)">
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/Downsampling2.png"></span>
              <figcaption>Figure 2</figcaption>
            </figure>
            <h2>Complexity calculation</h2>
            <p>
              After obtaining the downscaled simple polygon, various metrics can be computed to assess its complexity. 
              These metrics include the ratio of the downscaled boundary length to the original boundary length, 
              the ratio of the downscaled area to the original area enclosed by the boundary, L2 norm on the approximation error resulting from downsampling, 
              Hausdorff norm on the approximation error resulting from downsampling, error distributions between the downscaled and original boundaries, 
              curvature distributions at each downsampling level, tangent angle distributions and their changes at each downsampling level, 
              edge length distributions in the Voronoi diagram at each level, triangle area distributions in the Delaunay triangulation at each level, 
              and the percentage of Voronoi cell centers lying inside versus outside the shape at each level, 
              the area of the occupied downsampled image over the occupied area in the original image, among others. 
            </p>
            <p>
              In our system, we use the ratio of the downscaled boundary length to the original boundary length, 
              the ratio of the downscaled area to the original area to represent polygon complexity, it can be defined as:
            </p>
             <p v-html="renderedBlockFormula(`C_{downsamplingarea}= \\frac{S_{downscaled}}{S_{original}}`)"></p>
             <p v-html="renderedBlockFormula(`C_{downsamplingboundary}= \\frac{L_{downscaled}}{L_{original}}`)"></p>
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
name: "TheroyDownsampling",

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
  width: 1100px; /* 根据需求调整大小 */
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
