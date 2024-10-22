<template>
  <div>
    <h2>Please draw a polygon</h2>
    <canvas 
      ref="canvas"
      @click="drawPoint($event)" 
      width="500" 
      height="500"
      style="border: 1px solid black;">
    </canvas>
    <button @click="generatePolygon" :disabled="points.length < 3">Confirm!</button>
    <button @click="removeLastPoint" :disabled="points.length === 0">Delete!</button>

    <DataVisualization :responseData="responseData" />
  </div>
</template>

<script>
import axios from 'axios';
import DataVisualization from '../components/DataVisualization.vue';

export default {
  name: 'DrawPolygon',
  data() {
    return {
      points: [], // 保存多边形点的坐标
      responseData: null, // 存储后端返回的数据
    };
  },
  components: {
    DataVisualization,
  },
  methods: {
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

    // 将 Canvas 转换为图片并发送到后端
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

      try {
          // 上传文件到后端
        const response = await axios.post('http://localhost:5000/api/complexity', {
          type: 'points',  // 指定数据类型为多边形
          points: this.points, // 发送多边形的坐标
      });

          // 存储服务器返回的数据
      this.responseData = response.data;
      } catch (error) {
        console.error('上传失败:', error);
      }
    }
  },
};
</script>

<style scoped>
.response-data {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #42b983;
  background-color: #f9f9f9;
}
</style>
