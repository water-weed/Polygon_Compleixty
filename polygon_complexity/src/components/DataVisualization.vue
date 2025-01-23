<template>
  <div>
    <h2>Complexity</h2>
    <button @click="exportToExcel">Export</button>
    <table ref="table">
      <thead>
        <tr>
          <th>polygon</th>
          <!-- 动态生成表头，展示所有方法 -->
          <th>image</th>
          <th v-for="(method, index) in methods" :key="index" @click="sortTable(method)">
            {{ method }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(polygon, index) in sortedData" :key="index">
          <!-- 显示文件序号 -->
          <td>{{ polygon.fileName }}</td>
          <!-- 动态生成表格内容，展示每个方法的复杂度值 -->
          <td>
            <img :src="polygon.url" alt="Polygon Image" width="100" />
          </td>
          <td v-for="(method, i) in methods" :key="i">
            <a
              href="#"
              @click.prevent="navigateWithDetails(polygon, method)"
            >
            {{ getTotalComplexity(polygon.data, method) }}
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default {
  name: 'DataVisualization',
  props: {
    data: Array, // 传递从后端获取的多边形数据和复杂度信息
    urls:Object
  },
  data() {
    return {
      currentSortMethod: null, // 当前排序的列
      sortAscending: true // 排序方向，true为升序
    };
  },
  computed: {
    methods() {
    // 检查 data 数组是否存在，且至少包含一个文件
    if (this.data && this.data.length > 0) {
      //console.log(this.data);
      const firstFileData = this.data[0];
      const fileName = Object.keys(firstFileData)[0]; // 获取文件名 (如 file0, file1)

      // 检查文件名和多边形数据是否存在
      if (firstFileData[fileName] && typeof firstFileData[fileName] === 'object') {
        const samplePolygon = firstFileData[fileName]; // 获取第一个多边形的复杂度信息
        return Object.keys(samplePolygon); // 返回所有方法名 (如 DownsamplingBoundary, DownsamplingArea)
      }
    }
    return []; // 如果没有有效数据，返回空数组
  },
  sortedData() {
     // 防护检查，确保 this.data 存在且为数组
     if (!Array.isArray(this.data) || this.data.length === 0) {
      return []; // 如果 this.data 无效，返回空数组，避免错误
    }
    
    //print("url",this.urls);
    // 处理 polygons 的逻辑，类似于之前的代码
    const polygons = this.data.map(item => {
      const fileName = Object.keys(item)[0]; // 提取文件序号（例如 file0, file1）
      const data = item[fileName]; // 提取对应的复杂度数据
      const url = this.urls[fileName];
      return { fileName, data, url };
    });

    if (!this.currentSortMethod) {
      return polygons;
    }

    return [...polygons].sort((a, b) => {
      const complexityA = this.getTotalComplexity(a.data, this.currentSortMethod);
      const complexityB = this.getTotalComplexity(b.data, this.currentSortMethod);

      if (this.sortAscending) {
        return complexityA - complexityB;
      } else {
        return complexityB - complexityA;
      }
    });
  }
  },
  methods: {
    // 获取每个方法的总 complexity
    exportToExcel() {
      // 1. 获取表格数据
      const table = this.$refs.table;
      const workbook = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });

      // 2. 转换为 Excel 文件
      const excelBuffer = XLSX.write(workbook, {
        bookType: "xlsx",
        type: "array"
      });

      // 3. 创建 Blob 并下载
      const data = new Blob([excelBuffer], { type: "application/octet-stream" });
      saveAs(data, "table.xlsx");
    },
    
    getTotalComplexity(complexityData, method) {
      return (parseFloat(complexityData[method]?.complexity) || 0).toFixed(4); // 返回总的 complexity
    },

    // 排序表格
    sortTable(method) {
      if (this.currentSortMethod === method) {
        this.sortAscending = !this.sortAscending; // 切换排序方向
      } else {
        this.currentSortMethod = method; // 设置新的排序列
        this.sortAscending = true; // 默认升序
      }
    },

    navigateWithDetails(polygon, method) {
      const routeMap = {
        DownsamplingBoundary:{routeName:'DownsamplingBoundaryDetails'},
        DownsamplingArea:{routeName:'DownsamplingAreaDetails'},
        Boundary:{routeName:'BoundaryDetails'},
        Triangulation:{routeName:'TriangulationDetails'},
        Entropy:{routeName:'EntropyDetails'},
        Mat:{routeName:'MatDetails'},
        Edf:{routeName:'EdfDetails'},
        Weighted:{routeName:'WeightedDetails'},
      }

      const targetRoute = routeMap[method];

      if (!targetRoute){
        console.error('Unknown method:${method}');
        return;
      }

      this.$store.commit('setDetails', polygon.data[method]);

      this.$router.push({
        name: targetRoute.routeName,
        params: {
          fileName: polygon.fileName,
        },
        query: {
          complexity: this.getTotalComplexity(polygon.data, method),
        },
      });
    },
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px 12px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  cursor: pointer;
  background-color: #f2f2f2;
}
</style>
