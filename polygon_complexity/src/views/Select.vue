<<<<<<< HEAD
<!-- src/views/Select.vue -->
<template>
  <div class="select-container">
    <h2>Please select a polygon:</h2>.
    <SelectImage @upload-success="handleUploadSuccess" />

    <DataVisualization :responseData="responseData" />
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
    };
  },
  methods: {
    handleUploadSuccess(data) {
      this.responseData = data;
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
=======
<!-- src/views/Select.vue -->
<template>
  <div class="select-container">
    <h2>Please select a polygon:</h2>.
    <SelectImage @upload-success="handleUploadSuccess" />

    <DataVisualization :responseData="responseData" />
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
    };
  },
  methods: {
    handleUploadSuccess(data) {
      this.responseData = data;
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
>>>>>>> 9940b710187e10b903004c6d68852d2e6f417ace
</style>