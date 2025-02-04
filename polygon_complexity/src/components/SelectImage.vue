<!-- src/views/Select.vue -->
<template>
    <div class="image-gallery">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="image-item"
          :class="{ selected: displayImages.includes(image) }"
          @click="selectImage(image)"
        >
          <img :src="image.url" :alt="image.name" />
        </div>
    </div>
    <div class="button-container">
      <button @click="cancelSelection" :disabled="displayImages.length ===0">
        Cancel
      </button>
      <button @click="confirmSelection" :disabled="displayImages.length === 0">
        Ok
      </button>
    </div>
  </template>
  
  <script>
import axios from 'axios';
import { store } from '../store/store';

  export default {
    name: 'SelectImage',
    emits: ['upload-success'],
  
    data() {
      return {
        images: [], 
        selectedImage: null, 
        selectedImages:[],
        fileUrls:{},
        displayImages:[],
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
        const index = this.displayImages.indexOf(image);
        if (index === -1) {
          // if the image hasn't been chosen
          this.displayImages.push(image);
        } else {
          // if the image has been chosen, then deselect
          this.displayImages.splice(index,1);
        }
      },

      cancelSelection(){
        this.displayImages = [];
        this.selectedImages = [];
        this.fileUrls = {};
        this.$router.push({ name: 'System' });
      },

      async confirmSelection() {
        if (this.displayImages === 0) return;
  
        try {
          const formData = new FormData();
          formData.append('type', 'image');
          //console.log(this.displayImages);
          //console.log(this.selectedImages);
          this.selectedImages = this.selectedImages.concat(this.displayImages);
          //console.log(this.selectedImages);
          for (let [index, image] of this.selectedImages.entries()) {
            // get Blob Data
            const res = await fetch(image.url);  
            const blob = await res.blob();  
            const file = new File([blob], image.name, { type: blob.type });

            //formData.append(`file${index}`, file);
            formData.append(`file${store.n}`, file);
            //this.fileUrls[`file${index}`]= URL.createObjectURL(file);
            this.fileUrls[`file${store.n}`]= URL.createObjectURL(file);
            store.n++;
          }
          
          const response = await axios.post('http://localhost:5000/api/complexity', formData, {
          headers: {'Content-Type': 'multipart/form-data'}});

          const rawData = response.data.data;
          //console.log(rawData);
  
          // exchange to array
          const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
          });
          //console.log(this.fileUrls);
          this.$emit('upload-success', polygonData,this.fileUrls);
          this.$router.push({ name: 'System' });
        } catch (error) {
          console.error('Failure', error);
        }
        this.displayImages = [];
        this.selectedImages = [];
        this.fileUrls = {};
      }
    }
  };
  </script>
  
  <style scoped>
  
  .image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
    gap: 5px; 
    justify-items: center; 
    width: 100%;
    max-width: none; 
    max-width: 100%; /* 避免内容超出页面宽度 */
    overflow: auto; 
  }
  
  .image-item {
    border: 2px solid transparent;
    cursor: pointer;
  }
  
  .image-item img {
    width: 100%; /* 让图片充满 div */
    height: auto; /* 维持原始比例 */
    max-height: 100px; /* 避免太大 */
    object-fit: contain; /* 保证完整显示 */
  }
  
  .image-item.selected {
    border:5px solid #fdca6b;
  }
  
  button{
  border: 2px solid rgb(128, 68, 0);
  color: rgb(128, 68, 0);
}

button:hover{
  background-color: #fdca6b;
  color: white;
  border: none;
}

button:active{
  background-color: #fdca6b;
  color: #f9f9f9;
  border: none;
}
  
  .button-container {
  display: flex;
  justify-content: center; /* 居中对齐 */
  gap: 20px; /* 设置按钮间距 */
  margin-top: 15px;
}
  </style>