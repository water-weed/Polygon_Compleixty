<template>
    <div>
      <h1>DownsamplingArea details</h1>
      <p><strong>filename:</strong> {{ fileName }}</p>
      <p><strong>complexity:</strong> {{ complexity }}</p>
      <div>{{ details }}</div>
      <img :src="imageUrl" alt="Base64 Image" v-if="imageUrl" />
      <table border="1">
        <thead>
          <tr>
            <th>Sampling rate</th>
            <th>Complexity</th>
            <th>Original occupied pixels</th>
            <th>Total occupied pixels</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="key in sampleRate" :key="key">
            <td>{{ key }}</td>
            <td>{{ details[key].complexity }}</td>
            <td>{{ details[key].original_occupied_pixels }}</td>
            <td>{{ details[key].total_occupied_pixels }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data(){
      return{
        imageUrl:null,
      }
    },

    watch: {
    // 监听 details 数据的变化
    details: {
      handler(newDetails) {
        if (newDetails.img) {
          // 释放旧的 URL
          if (this.imageUrl) {
            URL.revokeObjectURL(this.imageUrl);
          }
          // 生成新的 URL
          this.imageUrl = this.createImageUrl(newDetails.img);
        }
      },
      immediate: true, // 立即执行一次，确保初始值
      deep: true, // 深度监听
    },
  },

    mounted() {
      this.imageUrl = this.createImageUrl(this.details.img);
      console.log(this.imageUrl);
    },
    //async mounted() {
    // 确保 details 数据加载完成后处理 img
    //this.$nextTick(() => {
      //if (this.details.img) {
        //this.imageUrl = this.createImageUrl(this.details.img);
      //}
    //});
  //},

    computed:{
      fileName(){
        return this.$route.params.fileName;
      },

      complexity(){
        return this.$route.query.complexity;
      },

      details(){
        return this.$store.getters.getDetails;
      },

      sampleRate(){
        const keys = Object.keys(this.details);
        return keys.filter(key => key !== "complexity" && key !== "img");
      }
    },

    methods:{
      createImageUrl(base64) {
      // 将 Base64 转换为 Blob
        const byteString = atob(base64.split(",")[1]); // 去掉前缀 "data:image/png;base64,"
        const mimeString = base64.split(",")[0].split(":")[1].split(";")[0]; // 提取 MIME 类型

      // 创建 Uint8Array 存储二进制数据
        const byteArray = new Uint8Array(byteString.length);
        for (let i = 0; i < byteString.length; i++) {
          byteArray[i] = byteString.charCodeAt(i);
        }

      // 创建 Blob 对象
        const blob = new Blob([byteArray], { type: mimeString });

      // 创建动态 URL
        const url = URL.createObjectURL(blob);
        //console.log(url);
        return url
    },
    }
  };
  </script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}
th, td {
  padding: 8px;
  border: 1px solid #ccc;
}
thead {
  background-color: #f4f4f4;
}
</style>