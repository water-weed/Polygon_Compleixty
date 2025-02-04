<template>
  <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 :fileUrl="excelUrl"/>

        <el-main class="content">
          <div class="content-wrapper">
            <div class="canvas-container">
              <canvas 
              ref="canvas"
              @click="drawPoint($event)" 
              width="700" 
              height="700"
              style="border: 1px solid black;"
              class="canvas">
              </canvas>

              <div class="button-group">
                <!---<button @click="generatePolygon" :disabled="points.length < 3">Finish</button>-->
                <button @click="removeLastPoint" :disabled="points.length === 0">Delete last node</button>
                <button @click="clearCanvas" :disabled="points.length ===0">Clear canvas</button>
                <!--<button @click="sendPolygons" :disabled="polygons.length === 0">Ok</button>-->
              </div>
            </div>

            <div class="button-container">
               <el-button  @click="cancelPolygon">
                Cancel
              </el-button>
              <el-button  @click="sendPolygons" :disabled="points.length < 3">
                Ok
              </el-button>
            </div>  
          </div>

    <!--<DataVisualization :data="responseData" :urls="fileUrls"/>-->
    <!--<ComplexityTable :data="responseData" :urls="fileUrls"/>-->
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios';
import Sidebar1 from '../components/Sidebar1.vue';
import PageHeader2 from '../components/PageHeader2.vue';
import DataTable from '../components/DataTable.vue';
import {store} from '../store/store';


export default {
  name: 'DrawPolygon',
  data() {
    return {
      points: [], // 保存多边形点的坐标
      polygons:[],
      responseData: null, // 存储后端返回的数据
      fileUrls:{},
      excelUrl:null,
      fileName:[],
    };
  },

  components: {
    Sidebar1,
    PageHeader2,
    DataTable,
  },
  methods: {
    updateExcelUrl(url) {
      this.excelUrl = url; // 更新父组件的 fileUrl
      console.log("Received fileUrl from DataTable:", url);
    },

    cancelPolygon(){
      this.points = []; // 保存多边形点的坐标
      this.polygons = [];
      this.fileUrls = {};
      this.fileName = [];
      const canvas = this.$refs.canvas;
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height); 
      this.$router.push({ name: 'System' });
    },

    // 绘制点，并将其保存到 points 数组中
    drawPoint(event) {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      const rect = canvas.getBoundingClientRect();

      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      // 绘制点
      ctx.fillStyle = 'black';
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fill();

      // 保存点坐标
      this.points.push({ x, y });

      // 画线，只连接当前点和前一个点
      if (this.points.length > 1) {
        const prevPoint = this.points[this.points.length - 2]; // 上一个点
        ctx.beginPath();
        ctx.moveTo(prevPoint.x, prevPoint.y); // 从上一个点开始
        ctx.lineTo(x, y); // 连接到当前点
        ctx.stroke();
      }
    },

    redrawCanvas() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');

      // 清空 Canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 重新绘制所有点和线
      for (let i = 0; i < this.points.length; i++) {
        const point = this.points[i];

        // 绘制每个点
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
        ctx.fill();

        // 连接每个点
        if (i > 0) {
          const prevPoint = this.points[i - 1];
          ctx.beginPath();
          ctx.moveTo(prevPoint.x, prevPoint.y);
          ctx.lineTo(point.x, point.y);
          ctx.stroke();
        }
      }
    },

    // 删除最后一个点并重新绘制 Canvas
    removeLastPoint() {
      if (this.points.length > 0) {
        this.points.pop(); // 删除最后一个点
        this.redrawCanvas(); // 重新绘制 Canvas
      }
    },

    // 将 Canvas 转换为图片
    async generatePolygon() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');

      // 如果有足够的点，绘制多边形最后一条边，连接最后一个点和第一个点
      if (this.points.length > 2) {
        const firstPoint = this.points[0];
        const lastPoint = this.points[this.points.length - 1];

        // 连接最后一个点到第一个点，形成闭合多边形
        ctx.beginPath();
        ctx.moveTo(lastPoint.x, lastPoint.y);
        ctx.lineTo(firstPoint.x, firstPoint.y);
        ctx.stroke();
      }

      
      //console.log(this.points);
      this.polygons.push(this.points);
      console.log(this.polygons);
      //console.log(this.polygons);
      //setTimeout(()=>{
        //ctx.clearRect(0, 0, canvas.width, canvas.height);
      //},1000);


      //生成多边形图片
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 700;
      tempCanvas.height = 700;
      const tempCtx = tempCanvas.getContext('2d');

      // 填充黑色背景
      tempCtx.fillStyle = "black";
      tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

      // 绘制白色多边形
      tempCtx.fillStyle = "white";
      tempCtx.beginPath();

      tempCtx.moveTo(this.points[0].x,this.points[0].y);
      //console.log(this.points[0].x,this.points[0].y)
      for(let i =1; i < this.points.length; i++){
        tempCtx.lineTo(this.points[i].x,this.points[i].y);
        //console.log(this.points[i].x,this.points[i].y);
      }

      //tempCtx.lineTo(this.points[0].x,this.points[0].y);
      tempCtx.closePath();
      tempCtx.fill();

      await new Promise((resolve, reject) => {
        tempCanvas.toBlob((blob) => {
          if (blob) {
            // 使用 URL.createObjectURL 生成图片 URL 并保存到 fileUrls 中
            this.fileUrls[`file${store.n}`] = URL.createObjectURL(blob);
            // 保存文件名到 fileName 数组中
            this.fileName.push(`file${store.n}`);
            store.n++;
            resolve();
          } else {
            reject(new Error("Blob creation failed"));
          }   
        }, "image/png");
      });

      /*tempCanvas.toBlob((blob) => {
        // 使用URL.createObjectURL生成图片URL
        this.fileUrls[`file${store.n}`] = URL.createObjectURL(blob);
        this.fileName.push(`file${store.n}`);
        store.n ++;
        //this.fileUrls[`file${store.n}`] = URL.createObjectURL(blob);
        //store.n ++;
      }, "image/png"); */

      this.points = []
      //console.log(this.points);
    },

    clearCanvas() {
    const canvas = this.$refs.canvas;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height); // 清除整个画布
    this.points = []; // 清空存储的点
    this.polygons = []; // 如果有存储的多边形，也清空
  },

    async sendPolygons(){
      await this.generatePolygon();
      console.log(this.polygons);
      console.log(this.fileName);
      const formData = new FormData();
      formData.append('type', 'points');

      this.polygons.forEach((polygon, index)=>{
        const polygonJSON = JSON.stringify(polygon);
        formData.append(this.fileName[index], polygonJSON); 
      });

      try {
        formData.forEach((value, key) => {
        console.log(key, value);
        });
        const response = await axios.post('http://localhost:5000/api/complexity', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          },
        /*const response = await axios.post('http://localhost:5000/api/complexity', {
          type: 'points',  // 指定数据类型为多边形
          points: this.polygons, // 发送多边形的坐标*/
      });

          // 存储服务器返回的数据
        const rawData = response.data.data;
        //console.log(rawData);
  
        // 将后端返回的对象转换为数组格式
        const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
        });

        // 将转换后的数据赋值给 this.responseData，以便传递给 DataVisualization 组件
        this.responseData = polygonData;
        store.polygonResult = [...store.polygonResult, ...this.responseData];
        store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
        //store.polygonResult = [...store.polygonResult, ...this.responseData.slice(store.polygonResult.length)];
        //console.log(store.polygonResult);
        //store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
        //console.log(store.polygonUrl);
        this.points = []; // 保存多边形点的坐标
        this.polygons = [];
        this.fileUrls = {};
        this.fileName = [];
        this.clearCanvas();
        this.$router.push({ name: 'System' });
      } catch (error) {
        console.error('Failure:', error);
      }
    }
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.response-data {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #fdca6b;;
  background-color: #f9f9f9;
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

.table-container {
  max-width: 100%;
  overflow-x: auto; /* 添加滚动条 */
}

.content-wrapper {
  max-width: 97%; /* 限制宽度 */
  overflow: auto; /* 让内容滚动 */
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; /* 与 DataTable 分开 */
}

.canvas-container {
  display: flex;
  align-items: center; /* 垂直居中 */
  gap: 20px; /* Canvas 和按钮之间的间距 */
  justify-content: center;
}

.button-group {
  display: flex;
  flex-direction: column; /* 让按钮垂直排列 */
  gap: 20px; /* 按钮之间的间距 */
  padding-left: 50px;
}

.button-group .el-button {
  width: 120px; /* 统一按钮宽度 */
}

.canvas{
  border:4px solid #fdca6b!important;
}

.button-container {
  display: flex;
  justify-content: center; /* 居中对齐 */
  gap: 20px; /* 设置按钮间距 */
  margin-top: 40px;
}
</style>
