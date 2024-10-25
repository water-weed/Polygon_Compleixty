<!-- src/views/Select.vue -->
<template>
  <div class="select-container">
    <h2>Please select a polygon:</h2>.
    <SelectImage @upload-success="handleUploadSuccess" />

    <DataVisualization :data="responseData" :urls="fileUrls"/>
  </div>
</template>

<script>
import DataVisualization from '../components/DataVisualization.vue';
import SelectImage from '../components/SelectImage.vue';

export default {
  name: 'Select',
  components: {
    SelectImage,  
    DataVisualization,
  },
  data() {
    return {
      responseData: null, 
      fileUrls:{}
    };
  },
  methods: {
    handleUploadSuccess(data,Urls) {
      this.responseData = data;
      this.fileUrls = Urls;
      //console.log(Urls);
    }
  }
};
</script>

<style scoped>
.select-container {
  text-align: center;
  padding: 20px;
  width: 100%;
  max-width: none; 
}
</style>