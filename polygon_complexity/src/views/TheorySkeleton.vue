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
              The skeleton of a polygon is a network of curves that captures and represents the internal structure of a polygonal. 
              For a given polygon, its skeleton typically consists of a set of line segments or curves that extend inward from the boundary and intersect 
              within the polygon, forming a treelike or graph-like structure. 
              The skeleton of a polygon is a crucial geometric structure that characterizes the internal configuration of the polygon. 
              It has a wide range of applications in shape analysis, shape simplification, path planning, and other fields. 
              By analyzing the polygon’s skeleton, the internal structure can be effectively captured, enabling the identification of symmetry, branching, 
              and other geometric features of the shape without being influenced by boundary details. 
              Due to its significance, many researchers have explored the development of global quantification methods for polygon complexity 
              based on different skeleton generation techniques.
            </p>
            <h2>Blum medial axis</h2>
            <p>The Blum Medial Axis is a curve formed by the centers of all the largest inscribed circles within a polygon. 
              It is the set of points inside the shape that maximizes the diameter of these inscribed circles. 
              This medial axis effectively captures the geometric structure of the shape, revealing key features such as protrusions, recesses, and branches. 
              Moreover, it provides a way to simplify the shape while preserving its fundamental characteristics. 
              As Figure 1 shows, the line is the Blum Medial Axis for a polygon.
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/skeleton1-1.jpg" class="img1"></span>
              <span><img src="../assets/skeleton1-2.png"></span>
              <figcaption>Figure 1</figcaption>
            </figure>
            <h2>Medial Axis Transform (MAT)</h2>
            <p>Based on the Blum Medial Axis, each skeleton point is associated with the radius of the inscribed circle at that point, 
              leading to the Medial Axis Transform (MAT). The medial axis is a method to simplify a shape while preserving its essential geometric characteristics. 
              By incorporating the radius attribute, the MAT provides a compact and efficient representation of the shape, 
              ensuring that no information is lost, as the original shape can be fully reconstructed from it. 
              Using the radius to characterize the properties of the medial axis, also known as the boundary distance function, it can be defined as:
            </p>
            <p v-html="renderedBlockFormula(`R(x)= \\min_{p\\in \\partial O} d(x,p)`)"></p>
            <p v-html="renderedInlineFormula(`That is, the shortest Euclidean distance from $x$ to the boundary $ \\partial O$, 
            which quantifies the extent of uniform shape expansion around $x$, as Figure 1 shows.`)">
            </p>
            <p>
              Costas Panagiotakis et al. proposed using MAT and entropy to quantify the complexity of polygons.
               With the radius of each node of skeleton, the complexity of polygon can be defined as:
            </p>
            <p v-html="renderedBlockFormula(`C_{MAT} = -\\sum_{i=1}^{n}p(r_i)logp(r_i)`)"></p>
            <p v-html="renderedInlineFormula(`Where $𝑟_𝑖 $ is the set of radius values for each node on the medial axis, and $𝑝(𝑟_𝑖)$ is the probability of each corresponding value.`)">
            </p>
            <h2>Extended Distance Function(EDF)</h2>
            <p>
              Although the MAT preserves the information of each node in the polygon’s skeleton, enabling the reconstruction of the original polygon, 
              the radius primarily reflects local thickness. Consequently, it is highly sensitive to noise along the polygon’s boundary. 
              To establish a global measure for characterizing the medial axis, Lu Liu et al. proposed the Extended Distance Function (EDF) 
              based on the boundary distance function. Unlike the boundary distance function, which mainly characterizes the local features of the medial axis, 
              the EDF focuses on capturing the global extensibility and main structure of the medial axis. As a result, it is more resistant to boundary noise.
            </p>
            <p v-html="renderedInlineFormula(`Unlike the boundary distance function, which uses Euclidean distance to define the radius of the media axis node,  
            the Extended distance function is defined as the radius of the longest 'tube' centered at a medial axis point that fits in the shape.  
            This characterizes the shape's ability to elongate or expand laterally at that point. Formally, let $x$ is a point on the shape $M$. For each 'axis' $f$ containing $f$ 
            (i.e., a path on the medial axis), the radius of the axis about $f$ is defined as:`)">
            </p>
            <p v-html="renderedBlockFormula(`r_f(x)=\\min_{y\\in \\partial f}(d_f(x,y)+R(y)) `)"></p>
            <p v-html="renderedInlineFormula(`Where $d_f(x,y)$ is the geodesic length from $x$ to $y$ along the axis $f$, 
            and $R(y)$ is the distance from the shape boundary to the point $y$. 
            Thus, the Extended Distance Function (EDF) at x can be defined as the maximum radius among all possible axes $f$:`)">
            </p>
            <p v-html="renderedBlockFormula(`\\tilde{R}(x)= \\sup_{f\\ni x}r_f(x)`)"></p>
            <p v-html="renderedInlineFormula(`The Extended Distance Function (EDF) can be computed using the grassfire transform. 
            This process involves first 'igniting a fire' at the shape's boundary, allowing it to propagate inward until it reaches the medial axis. 
            Then, a second wave of fire is ignited from the endpoints of the medial axis and propagates along the axis at a uniform speed. 
            The EDF value at a given point corresponds to the time it takes for the fire to reach that point. 
            Through this computation, the EDF value at $x$ can also be interpreted as the geodesic distance from the shape boundary to $x$ along the medial axis, as Figure 2 shows.`)">
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/skeleton1-1.jpg" class="img1"></span>
              <span><img src="../assets/skeleton2-2.png"></span>
              <figcaption>Figure 2</figcaption>
            </figure>
            <p>Similar to the Medial Axis Transform (MAT), we can incorporate entropy to quantify the complexity of a polygon. That is:</p>
            <p v-html="renderedBlockFormula(`C_{EDF} = -\\sum_{i=1}^{n}p(e _i)logp(e _i) `)"></p>
            <p v-html="renderedInlineFormula(`Where $e_𝑖 $ is the set of EDF values for each node on the medial axis, and $𝑝(e_𝑖)$ is the probability of each corresponding value.`)"></p>
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
name: "TheorySkeleton",

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
