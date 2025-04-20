<template>
  <div class="container">
    <el-container>
      <Sidebar1 />
      <el-container class="main-content">
        <PageHeader2 :fileUrl="excelUrl"/>
         <!--canvas-->
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

              <!--button-->
              <div class="button-container">
               <el-button  @click="cancelPolygon">
                Cancel
              </el-button>
              <el-button  @click="sendPolygons" :disabled="points.length < 3">
                Ok
              </el-button>
            </div> 

              <!--<div class="button-group">
                <button @click="removeLastPoint" :disabled="points.length === 0">Delete last node</button>
                <button @click="clearCanvas" :disabled="points.length ===0">Clear canvas</button>
              </div>-->
            </div>

            <!--<div class="button-container">
               <el-button  @click="cancelPolygon">
                Cancel
              </el-button>
              <el-button  @click="sendPolygons" :disabled="points.length < 3">
                Ok
              </el-button>
            </div>  -->
            <div class="button-group">
              <button @click="removeLastPoint" :disabled="points.length === 0">Delete last node</button>
              <button @click="clearCanvas" :disabled="points.length ===0">Clear canvas</button>
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
      points: [], // coordinates of polygon points
      polygons:[],
      responseData: null, // data from backend
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
      this.excelUrl = url; // update the parent component's fileUrl
      console.log("Received fileUrl from DataTable:", url);
    },

    //cancel function
    cancelPolygon(){
      this.points = []; 
      this.polygons = [];
      this.fileUrls = {};
      this.fileName = [];
      const canvas = this.$refs.canvas;
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height); 
      this.$router.push({ name: 'System' });
    },

    // Draw the points and save them in the points array
    drawPoint(event) {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      const rect = canvas.getBoundingClientRect();

      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      // draw points
      ctx.fillStyle = 'black';
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fill();

      // save coordinates
      this.points.push({ x, y });

      // draw line, connect current points to previous points
      if (this.points.length > 1) {
        const prevPoint = this.points[this.points.length - 2]; // previous points
        ctx.beginPath();
        ctx.moveTo(prevPoint.x, prevPoint.y); 
        ctx.lineTo(x, y); // connect
        ctx.stroke();
      }
    },

    //redraw canvas
    redrawCanvas() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');

      //clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // redraw all the line and points
      for (let i = 0; i < this.points.length; i++) {
        const point = this.points[i];

        // draw points
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
        ctx.fill();

        // connect every points
        if (i > 0) {
          const prevPoint = this.points[i - 1];
          ctx.beginPath();
          ctx.moveTo(prevPoint.x, prevPoint.y);
          ctx.lineTo(point.x, point.y);
          ctx.stroke();
        }
      }
    },

    // delete last points and redraw canvas
    removeLastPoint() {
      if (this.points.length > 0) {
        this.points.pop(); // delete last points
        this.redrawCanvas(); // redraw Canvas
      }
    },

    // convert canvas to images
    async generatePolygon() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');

      // if have enough points, draw the last line of polygons
      if (this.points.length > 2) {
        const firstPoint = this.points[0];
        const lastPoint = this.points[this.points.length - 1];

        // connect the last point to the first point
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


      //generate polygon image
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 700;
      tempCanvas.height = 700;
      const tempCtx = tempCanvas.getContext('2d');

      // fill black background
      tempCtx.fillStyle = "black";
      tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

      // draw white polygon
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
            // use URL.createObjectURL generate image URL and save in fileUrls
            this.fileUrls[`file${store.n}`] = URL.createObjectURL(blob);
            // save file name in fileName array
            this.fileName.push(`file${store.n}`);
            store.n++;
            resolve();
          } else {
            reject(new Error("Blob creation failed"));
          }   
        }, "image/png");
      });

      /*tempCanvas.toBlob((blob) => 
        this.fileUrls[`file${store.n}`] = URL.createObjectURL(blob);
        this.fileName.push(`file${store.n}`);
        store.n ++;
        //this.fileUrls[`file${store.n}`] = URL.createObjectURL(blob);
        //store.n ++;
      }, "image/png"); */

      this.points = []
      //console.log(this.points);
    },

    //clear canvas
    clearCanvas() {
    const canvas = this.$refs.canvas;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height); // clear canvas
    this.points = []; // clear saved points
    this.polygons = []; // clear save polygons
  },

  //send polygon to backend
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
          type: 'points',  
          points: this.polygons, */
      });

          // save data from backend
        const rawData = response.data.data;
        //console.log(rawData);
  
        // convert object from backend to arrary type
        const polygonData = Object.keys(rawData).map(fileName => {
          return { [fileName]: rawData[fileName] };
        });

        this.responseData = polygonData;
        store.polygonResult = [...store.polygonResult, ...this.responseData];
        store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
        //store.polygonResult = [...store.polygonResult, ...this.responseData.slice(store.polygonResult.length)];
        //console.log(store.polygonResult);
        //store.polygonUrl = {...store.polygonUrl, ...this.fileUrls};
        //console.log(store.polygonUrl);
        this.points = []; 
        this.polygons = [];
        this.fileUrls = {};
        this.fileName = [];
        this.clearCanvas();//clear all data
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

/* main content */
.content {
  padding: 20px;
  text-align: center;
  background-color: #f5f5f5;
  flex-grow: 1;
  width: 100%;
}

/*button style*/
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
  overflow-x: auto; 
}

/*canvas style*/
.content-wrapper {
  max-width: 97%; 
  background: #fff;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; 
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.canvas-container {
  display: flex;
  align-items: center; 
  gap: 20px; 
  flex-direction: column;
}

.button-group {
  display: flex;
  flex-direction: column; 
  gap: 20px;
  padding-left: 20px;
}

.button-group .el-button {
  width: 120px; 
}

.canvas{
  border:4px solid #fdca6b!important;
}

.button-container {
  display: flex;
  justify-content: center; 
  gap: 20px; 
  margin-top: 40px;
  width: 100%;
  align-items: center;
}
</style>
