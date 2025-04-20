<!-- src/views/Select.vue -->
<template>
    <div class="image-gallery">
      <!--image display-->
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
      <!-- button:cancel and confirm -->
    <div class="button-container">
      <button @click="cancelSelection">
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
    emits: ['upload-success'], // Parent component listens for upload completion events
  
    data() {
      return {
        images: [], //image object
        selectedImages:[], //uploaded images
        fileUrls:{}, //file name of uploaded images
        displayImages:[], //selected images
      };
    },
  
    created() {
      this.loadImages(); //load all images
    },
  
    methods: {
      //dynamically import all .gif images in the specified path
      loadImages() {
        const imageModules = import.meta.glob('../assets/select_images/*.gif');
        
        for (const path in imageModules) {
          imageModules[path]().then((module) => {
            const image = {
              name: path.split('/').pop(), //extract file name
              url: module.default //image url
            };
            this.images.push(image);
          });
        }
      },

      //function of selecting image
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

      //cancel all selection and return to system page
      cancelSelection(){
        this.displayImages = [];
        this.selectedImages = [];
        this.fileUrls = {};
        this.$router.push({ name: 'System' });
      },

      //confirm selection, upload image and return to system page 
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
          
          //connect backend
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

        //reset
        this.displayImages = [];
        this.selectedImages = [];
        this.fileUrls = {};
      }
    }
  };
  </script>
  
  <style scoped>
  /* image grid layout */
  .image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
    gap: 5px; 
    justify-items: center; 
    width: 100%;
    max-width: none; 
    max-width: 100%; 
    overflow: auto; 
  }
  
  /*every image cell*/
  .image-item {
    border: 2px solid transparent;
    cursor: pointer;
  }
  
  /*image*/
  .image-item img {
    width: 100%; 
    height: auto; 
    max-height: 100px; 
    object-fit: contain; 
  }
  
  /*selected image border*/
  .image-item.selected {
    border:5px solid #fdca6b;
  }
  
  /*button*/
  button{
  border: 2px solid rgb(128, 68, 0);
  color: rgb(128, 68, 0);
}

/*hover button */
button:hover{
  background-color: #fdca6b;
  color: white;
  border: none;
}

/*active button*/
button:active{
  background-color: #fdca6b;
  color: #f9f9f9;
  border: none;
}

/*button container */
  .button-container {
  display: flex;
  justify-content: center; 
  gap: 20px;
  margin-top: 15px;
}
  </style>