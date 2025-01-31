<!-- 📂 src/components/PageHeader.vue -->
<template>
    <div class="page-header">
        <div class="header-left">
            <h1>System</h1>
        </div>
        <div class="header-right">
            <button class="header-btn" @click="handleSelect"  v-tippy="{content:'Select polygons from preload list', theme:'page-header', arrow: false,}">
                <font-awesome-icon :icon="['fas', 'list-check']" />
            </button>
            <button class="header-btn" @click="handleUpload" v-tippy="{content:'Upload polygon files', theme:'page-header', arrow: false,}">
                <font-awesome-icon :icon="['fas', 'upload']" />
            </button>
            <button class="header-btn" @click="handleDraw" v-tippy="{content:'Draw some polygons by yourself',theme:'page-header', arrow: false,}">
                <font-awesome-icon :icon="['fas', 'pencil']" />
            </button>
            <button class="header-btn" @click="handleExport" v-tippy="{content:'Export the complexity table', theme:'page-header', arrow: false,}">
                <font-awesome-icon :icon="['fas', 'file-export']" />
            </button>
        </div>
    </div>
</template>
  
<script>

  export default {
    name: "PageHeader2",

    props:{
      fileUrl:String,
    },

    methods: {
    handleSelect() {
        this.$router.push('/Select'); 
    },
    handleUpload() {
        this.$router.push('/Upload');
    },
    handleExport() {
      if (!this.fileUrl) return;

const link = document.createElement("a");
link.href = this.fileUrl;
link.setAttribute("download", "exported_data.xlsx");
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
},


    handleDraw() {
        this.$router.push('/Draw');
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
  box-sizing: border-box;
  justify-content: space-between; 
  gap: 10px; 
  padding: 10px 20px 10px 10px;
}

.header-left {
  display: flex;
  align-items: center;
  padding-left: 20px
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px; /* 按钮间距 */
}

.header-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 20px;
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%; /* 圆形按钮 */
  width: 60px;
  height: 60px;
  color: rgb(100, 53, 0);
  transition: background-color 0.2s ease;
  border: none;
  outline: none;
}

.header-btn:hover {
  background-color: #fcebcd; /* 鼠标悬停时背景色 */
}

.header-btn:active {
  background-color: #fde0aa;; /* 激活时背景色 */
  transform: scale(0.95); /* 点击时缩小效果 */
}

.icon {
  font-size: 18px;
}

:deep(.tippy-box[data-theme~='page-header']) {
  background-color: #a5c2be; /* Tooltip 背景色 */
  color: #ffffff; /* Tooltip 字体颜色 */
  border-radius: 8px; /* 圆角 */
  font-size: 20px; /* 字体大小 */
  padding: 5px 10px;
  opacity: 0.9;
  transform: translateY(10px);
}
</style>
  