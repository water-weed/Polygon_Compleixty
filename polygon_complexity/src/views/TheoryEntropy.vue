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
              Information theory is a mathematical framework launched by Claude Shannon. 
              It deals with the quantification, transmission, coding, and processing of information. 
              It is not only the cornerstone of communication system design but also plays an important role in data compression, encryption, machine learning, 
              and other fields. The theory fundamentally explores how to measure and describe the uncertainty, redundancy, and structure of data.
              When we analyze polygons, 
              these shapes are treated as complete images where the degree of uncertainty and chaos within the image information determines the complexity of the polygon. 
              A polygon with high levels of uncertain and chaotic information is considered more complex, 
              as it poses greater challenges for operational modifications or analytical computations. 
              Therefore, many researchers have begun to apply concepts from information theory to the analysis of polygonal images. 
              This approach allows for a different understanding of polygon complexity, 
              where the focus is on evaluating the information inherent in the polygon rather than just its geometric or topological features.
            </p>
            <p v-html="renderedInlineFormula(`In information theory, one of the most basic concepts is information entropy, also known as Shannon entropy. 
            Information entropy was proposed by Claude Shannon to measure the uncertainty of an information source.
            For a discrete random variable $X$, which can take on values from a set $\\{x_1, x_2,\\dots,x_n\\}$, 
            with corresponding probabilities$\{p(x_1), p(x_2),\\dots,p(x_n)\}$, the entropy $H(X)$ is defined as:`)">
            </p>
            <p v-html="renderedBlockFormula(`H(X) = -\\sum_{i=1}^{n}p(x_i)logp(x_i)`)"></p>
            <p>
              In the field of image processing, entropy can be used for quantifying the complexity and information content of an image. 
              It effectively measures the randomness or unpredictability of the image content. 
              Images that are more uncertain or chaotic exhibit higher information entropy, often perceived as being more complex. 
              Therefore, some researchers use information entropy to define the complexity of polygons. 
              Regarding polygons, we need to select an appropriate attribute of the polygon that captures this uncertainty or chaos to define the complexity. 
              Researchers DL Page et al. and N Volarevic et al. both focused on the curvature of the polygon as a crucial characteristic for this purpose.
            </p>
            <h2>Curvature</h2>
            <p v-html="renderedInlineFormula(`For a polygon $P$, it has a set of vertices $\{P_1,P_2,\\dots,P_n\}$. 
            For the curvature  $\\kappa _i$ of each vertex $P_i$, it is directly proportional to the turning angle $\\theta _i$, 
            formed by the line segments from endpoint $P_{i-1}$ to endpoint $P_i$ and from $P_i$ to $P_{i+1}$. 
            As the Figure 1 shows, so we can use $\\theta$ to represent the $\\kappa_i$ of $P_i$.`)">
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/Entropy1.png"></span>
              <figcaption>Figure 1</figcaption>
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
            <h2>Complexity calculation</h2>
            <p v-html="renderedInlineFormula(`We can calculate the curvature $\\kappa_i$ of every vertex $P_i$ and get the probability distribution of 
            curvature for polygon $P$. As mentioned before, the complexity is defined through entropy $ H(X) = -\\sum_{i=1}^{n}p(x_i)logp(x_i)$, 
            where $p(x_i)$ is the probability of certain vertex curvature $\\kappa$. Figure 2 shows an example of this.`)">
            </p>
            <figure class="image-with-caption">
              <span><img src="../assets/preload_images/file17.jpg" class="img1"></span>
              <span><img src="../assets/entropy2.png"></span>
              <figcaption>Figure 2</figcaption>
            </figure>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader1 from '../components/PageHeader1.vue';
import katex from "katex";
import "katex/dist/katex.min.css";


export default {
name: "TheoryEntropy",

components: {
  Sidebar1,
  PageHeader1,
},

methods: {
  //inline formula
  renderedInlineFormula(inlineText) {
      return inlineText.replace(/\$(.*?)\$/g, (match, formula) =>
        katex.renderToString(formula, { throwOnError: false, displayMode: false })
      );
    },

    //block formula
    renderedBlockFormula(blockFormula) {
      return katex.renderToString(blockFormula, { throwOnError: false, displayMode: true });
    }
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Edu+TAS+Beginner:wght@400..700&display=swap');
/*page layout sytle*/
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
}

.introduction {
  max-width: 90%;
  margin: auto;
  text-align: left;
}

/* title style */
h2, h3 {
  margin-bottom: 10px;
  color: #00443c;
}

/*text style */
p {
  font-size: 30px;
  line-height: 1.6;
  color: rgb(128, 68, 0);
  font-family: "Edu TAS Beginner", serif;
  font-optical-sizing: auto;
}

/*image style*/
.image-with-caption {
  display: inline-block;
  flex-direction: column;
  align-items: center; 
  justify-content: center; 
  text-align: center; 
  width: 100%; 
}

.image-with-caption img {
  width: 40%; 
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

/*formula style*/
:deep(.katex){
  font-family: "Edu TAS Beginner", serif!important;
  font-optical-sizing: auto!important;
}

.formula-block {
  text-align: center;
  margin: 10px 10px;
}

.img1{
  width:30%!important;
}
</style>
