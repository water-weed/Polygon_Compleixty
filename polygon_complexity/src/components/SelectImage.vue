<!-- src/views/Select.vue -->
<template>
    <div class="image-gallery">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="image-item"
          :class="{ selected: selectedImages.includes(image) }"
          @click="selectImage(image)"
        >
          <img :src="image.url" :alt="image.name" />
        </div>
    </div>
      <button @click="confirmSelection" :disabled="selectedImages.length === 0">
        Confirm!
      </button>
  </template>
  
  <script>
import axios from 'axios';

  export default {
    name: 'SelectImage',
    emits: ['upload-success'],
  
    data() {
      return {
        images: [], 
        selectedImage: null, 
        selectedImages:[]
      };
    },
  
    created() {
      this.loadImages(); 
    },
  
    methods: {
      loadImages() {
        const imageModules = import.meta.glob('../assets/select_images/*.gif');
        
        for (const path in imageModules) {
          imageModules[path]().then((module) => {
            const image = {
              name: path.split('/').pop(), 
              url: module.default 
            };
            this.images.push(image);
          });
        }
      },
  
      selectImage(image) {
        const index = this.selectedImages.indexOf(image);
        if (index === -1) {
          // if the image hasn't been chosen
          this.selectedImages.push(image);
        } else {
          // if the image has been chosen, then deselect
          this.selectedImages.splice(index, 1);
        }
      },

      async confirmSelection() {
        if (this.selectedImages === 0) return;
  
        try {
          const formData = new FormData();
          formData.append('type', 'image');
          for (let [index, image] of this.selectedImages.entries()) {
            // get Blob Data
            const res = await fetch(image.url);  
            const blob = await res.blob();  
            const file = new File([blob], image.name, { type: blob.type });

            
            formData.append(`file${index}`, file);
          }
          
          const response = await axios.post('http://localhost:5000/api/complexity', formData, {
          headers: {'Content-Type': 'multipart/form-data'}});

          const rawData = response.data.data;
          console.log(rawData);
  
          // exchange to array
          const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
          });

          this.$emit('upload-success', polygonData);
        } catch (error) {
          console.error('Failure', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  
  .image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
    gap: 15px; 
    justify-items: center; 
    width: 100%;
    max-width: none; 
  }
  
  .image-item {
    border: 2px solid transparent;
    cursor: pointer;
  }
  
  .image-item img {
    width: 140px;
    height: 120px;
    object-fit: cover;
    transition: transform 0.3s;
  }
  
  .image-item:hover img {
    transform: scale(1.1);
  }
  
  .image-item.selected {
    border-color: #42b983;
  }
  
  button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>