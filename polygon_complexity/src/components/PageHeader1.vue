<!-- Page header for Home, System, Theory, About page -->
<template>
    <div class="page-header">
      <h1>{{ pageTitle }}</h1>
    </div>
  </template>
  
  <script>
  export default {
    name: "PageHeader1",

    data() {
      return {
        currentFunction: "Select Function", // current data input method
        menuItems: [
          { name: "Select", label: "Select Polygon" },
          { name: "Upload", label: "Upload Polygon" },
          { name: "Draw", label: "Draw Polygon" },
        ],
      };
    },

    //navigation table
    computed: {
      pageTitle() {
        const routeName = this.$route.name;
        const titles = {
          Home1: "Home",
          SystemDescription: "System description",
          TheroyDownsampling: "Downsampling",
          TheoryBoundary:"Boundary",
          TheoryTriangulation:"Triangulation",
          TheoryEntropy:"Entropy",
          TheorySkeleton:"Skeleton",
          TheoryWeighted:"Weighted",
          About: "About us",
          Select:"Select a polygon",
          Upload:"Upload a polygon",
          Draw:"Draw a polygon",
          System:"Polygon complexity System",
        };
        return titles[routeName] || "Unnamed page";
      },
    },
};
</script>
  
<style scoped>.page-header {
  position: relative;
  width: 100%; 
  height: 80px; 
  background-color: #fdca6b;
  color: white;
  display: flex;
  align-items: center;
  font-size: 10px;
  box-shadow: 0px 2px 5px white;
  flex-shrink: 0;
  padding-left: 20px;
  box-sizing: border-box
}
</style>
  