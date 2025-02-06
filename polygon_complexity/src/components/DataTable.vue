<template>
    <div>
        <el-checkbox-group v-model="visibleMethods" >
        <el-checkbox
          v-for="(method, index) in methods"
          :key="index"
          :value="method"
        >
          {{ method }}
        </el-checkbox>
      </el-checkbox-group>

      <!-- 表格 -->
      <el-table
        :data="sortedData"
        border
        style="width: 100%"
        v-if="sortedData.length"
        :key="tableKey"
        :fit = "true"
      >

        <!-- 固定的 polygon 列 -->
        <el-table-column prop="fileName" label="Polygon"/>
  
        <!-- 固定的 image 列 -->
        <el-table-column label="Image">
          <template #default="scope">
            <img :src="scope.row.url" alt="Polygon Image" style="max-width: 100%; height: auto; display: block;" />
          </template>
        </el-table-column>
  
        <!-- 动态生成的列 -->
        <el-table-column
          v-for="(method, index) in visibleMethods"
          :key="index"
          :prop="method"
          :label="method"
          sortable
          @sort-change="handleSortChange"
          :row-key="row => row.fileName"
        >
          <template #default="scope">
            <a
              href="#"
              @click.prevent="navigateWithDetails(scope.row, method)"
            >
              {{ getTotalComplexity(scope.row.data, method) }}
            </a>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
<script>
import Sortable from 'sortablejs';
import preload1Img from '../assets/preload_images/file6.jpg';
import preload2Img from '../assets/preload_images/file17.jpg';
import axios from "axios";
import ExcelJS from "exceljs";


  export default {
    name: 'DataTable',
    props: {
      data: Array,
      urls:Object,
    },
    data() {
      return {
        visibleMethods: [], // 可见的列
        sortKey: "", // 当前排序字段
        sortOrder: 1, // 排序顺序：1为升序，-1为降序
        tableKey: 0,
        displayData: [], 
        displayUrls:{},
        fileUrl:null,
        /*initialData: [ // 示例数据
        {
          preload1:{
            DownsamplingBoundary: {complexity: 0.552},
            DownsamplingArea: {complexity: 0.0827} ,
            Boundary: {complexity:0.00255},
            Triangulation:{complexity:0},
            Entropy:{complexity:2.1556},
            Edf:{complexity:6.0784},
            Mat:{complexity:6.1528},
            Weighted:{complexity:0.0311},
          },
        },
        {
          preload2: {
            DownsamplingBoundary: { complexity: 0.3460 },
            DownsamplingArea: { complexity: 0.1984 },
            Boundary: { complexity: 0.0042 },
            Triangulation:{complexity:0},
            Entropy:{complexity:2.9385},
            Edf:{complexity:6.6540},
            Mat:{complexity:6.7886},
            Weighted:{complexity:0.3963},
          },
        },
      ],*/
      initialData:[],
      initialUrls:{
        preload1: preload1Img,
        preload2: preload2Img,
      }
      };
    },

    mounted() {
      // 在组件挂载后初始化 visibleMethods
      //console.log("methods:", this.methods);
      axios.get('http://localhost:5000/api/complexity').then(
        response =>{
          const rawData = response.data.data;
          //console.log(rawData);
  
          // 将后端返回的对象转换为数组格式
          const polygonData = Object.keys(rawData).map(fileName => {
            return { [fileName]: rawData[fileName] };
          });
          this.initialData = polygonData;
          this.displayData = [...this.initialData]; // 使用初始数据填充表格
          this.displayUrls = { ...this.initialUrls };
          this.visibleMethods = this.methods;

          this.$nextTick(() => {
            this.initSortable(); // 确保拖动初始化在 DOM 渲染完成后执行
            });
        }
      )
      //this.displayData = [...this.initialData]; // 使用初始数据填充表格
      //this.displayUrls = { ...this.initialUrls };
      //this.visibleMethods = this.methods;
      //console.log(this.visibleMethods);
    },

    watch: {
    // 监听表格数据的变化
    data: {
      immediate: true,
      handler(newData) {
        if (newData && newData.length > 0) {
          this.addDataToTable(newData);
          this.visibleMethods = this.methods;
          //console.log(this.visibleMethods);
          this.$nextTick(() => {
            this.initSortable();
          });
        }
        this.handleExport();
    },
  },
    
    visibleMethods: {
      handler() {
        // 表头顺序变化后强制触发重新渲染
        if(this.visibleMethods){
          //console.log(this.visibleMethods);
        }
        this.handleExport();
      },
      deep: true,
    },

    tableKey() {
    this.$nextTick(() => {
      this.initSortable();
    });
  },
  },

    computed: {
        methods() {
          // 检查 data 数组是否存在，且至少包含一个文件
          if (this.displayData && this.displayData.length > 0) {
            //console.log(this.data);
            const firstFileData = this.displayData[0];
            const fileName = Object.keys(firstFileData)[0]; // 获取文件名 (如 file0, file1)
            // 检查文件名和多边形数据是否存在
            if (firstFileData[fileName] && typeof firstFileData[fileName] === 'object') {
              const samplePolygon = firstFileData[fileName]; // 获取第一个多边形的复杂度信息
              return Object.keys(samplePolygon); // 返回所有方法名 (如 DownsamplingBoundary, DownsamplingArea)
              }
            }
            return []; // 如果没有有效数据，返回空数组
          },

      // 排序后的数据
      sortedData() {
        if (!Array.isArray(this.displayData) || this.displayData.length === 0) {
          return []; // 如果 this.data 无效，返回空数组，避免错误
        }

        const polygons = this.displayData.map(item => {
          const fileName = Object.keys(item)[0]; // 提取文件序号（例如 file0, file1）
          const data = item[fileName]; // 提取对应的复杂度数据
          //console.log(data);
          const url = this.displayUrls[fileName];
          return { fileName, data, url };
        });

        console.log(polygons);

        if (!this.sortKey) return polygons;
  
        return [...polygons].sort((a, b) => {
          const aValue = this.getTotalComplexity(a.data, this.sortKey);
          const bValue = this.getTotalComplexity(b.data, this.sortKey);
  
          if (aValue < bValue) return -1 * this.sortOrder;
          if (aValue > bValue) return 1 * this.sortOrder;
          return 0;
        });
      },
    },

    methods: {
      // 计算复杂度
      getTotalComplexity(data, method) {
        //console.log(data);
        //console.log(method),
        //console.log(data[method].complexity);
        return (parseFloat(data[method].complexity ?? 0)).toFixed(4); // 如果没有值，返回 0
      },

      // 处理排序
      handleSortChange({ prop, order }) {
        this.sortKey = prop;
        this.sortOrder = order === "ascending" ? 1 : -1;
      },

      addDataToTable(newData) {
        //console.log('Adding new data to table:', newData);
        // 合并新数据到 displayData
        //this.displayData = this.displayData.concat(newData);
        this.displayData = [...this.initialData,...newData];
        this.displayUrls = {
          ...this.initialUrls, // 保留现有的 URLs
          ...this.urls, // 添加或更新新 URLs
        };
        console.log('Updated displayData:', this.displayData);
        console.log(this.urls);
        console.log(this.displayUrls);
      },

      // 点击某个复杂度时的操作
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

    async handleExport() {
        const workbook = new ExcelJS.Workbook();
        const sheet = workbook.addWorksheet("Table Data");
        
        // 设置表头
        sheet.addRow(["Polygon", "Image", ...this.visibleMethods]);
        
        // 填充数据
        for (let i = 0; i < this.sortedData.length; i++) {
            const row = this.sortedData[i];
            const newRow = [row.fileName, "", ...this.visibleMethods.map((method) => row.data[method].complexity ?? "")];
            sheet.addRow(newRow);
            
            // 嵌入图片
            const imageResponse = await axios.get(row.url, { responseType: "arraybuffer" });
            const imageId = workbook.addImage({
                buffer: imageResponse.data,
                extension: "png",
            });
            
            sheet.addImage(imageId, {
                tl: { col: 1, row: i + 1 }, // 左上角
                ext: { width: 50, height: 50 }, // 图片尺寸
            });
        }
        
        // 导出文件
        const buffer = await workbook.xlsx.writeBuffer();
        const blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
       
        if (this.fileUrl) {
          URL.revokeObjectURL(this.fileUrl); // 清除旧的 Blob URL
        }
        this.fileUrl = URL.createObjectURL(blob); // 生成新的 Blob URL
        //console.log(this.fileUrl);
        this.$emit("file-generated", this.fileUrl);
      },

    initSortable() {
      const container = this.$el.querySelector(".el-table__header-wrapper tr");

      if (!container) {
        console.error("Sortable initialization failed: Header container not found");
        return;
      }

      console.log("Initializing Sortable.js on:", container);


      Sortable.create(container, {
        animation: 150,
        onEnd: (event) => {
          console.log("Old index:", event.oldIndex, "New index:", event.newIndex);
          console.log("Before change:", this.visibleMethods);

          const oldIndex = event.oldIndex-2;
          const newIndex = event.newIndex-2;

          // 更新 visibleMethods 的顺序
          //const movedMethod = this.visibleMethods.splice(oldIndex, 1)[0];
          //this.visibleMethods.splice(newIndex, 0, movedMethod);

          //console.log("After change:", this.visibleMethods);

          // 触发 Vue 的响应式更新
          //this.visibleMethods = [...this.visibleMethods];
          //console.log("After change:", this.visibleMethods);

          const oldItem = this.visibleMethods[oldIndex];
          const newItem = this.visibleMethods[newIndex];
          console.log(oldItem);
          console.log(newItem)
          console.log(oldIndex);
          this.visibleMethods[oldIndex] = newItem;
          console.log(this.visibleMethods);
          this.visibleMethods[newIndex] = oldItem;
          //his.visibleMethods.splice(oldIndex,1);
          //console.log(this.visibleMethods);
          //this.visibleMethods.splice(newIndex,0,oldItem);
          console.log("After change:", this.visibleMethods);
          
          this.visibleMethods = [...this.visibleMethods];
          this.tableKey += 1;
        },
      });
    },
  },
};
</script>

<style scoped>
/* 修改 checkbox 的颜色 */
:deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: rgb(100, 53, 0); /* 修改选中时的文字颜色 */
  font-size: 19px;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: rgb(100, 53, 0); /* 修改选中时的背景颜色 */
  border-color: rgb(100, 53, 0); /* 修改选中时的边框颜色 */
}

:deep(.el-checkbox__input:not(.is-checked) + .el-checkbox__label) {
  color: #a5c2be; /* 设置未选中状态的字体颜色 */
  font-size: 19px;
}

:deep(.el-checkbox__inner) {
  border-color: #a5c2be; /* 设置未选中状态的边框颜色 */
}

:deep(.el-table) {
  font-size: 14px; /* 设置表格字体大小 */
}

/* 表头字体颜色 */
:deep(.el-table__header-wrapper th) {
  color: #a5c2be; /* 修改表头字体颜色 */
}

/* 表格内容字体颜色 */
:deep(.el-table__body-wrapper td) {
  color: rgb(100, 53, 0); /* 修改表格内容字体颜色 */
}

/* 修改表格内链接颜色 */
:deep(.el-table__body-wrapper a) {
  color: rgb(100, 53, 0); /* 设置链接默认颜色 */
  text-decoration: none; /* 去掉下划线 */
}

/* 修改表格内链接 hover 时的颜色 */
:deep(.el-table__body-wrapper a:hover) {
  color: #fdca6b;; /* 鼠标悬停时的颜色 */
  text-decoration: underline; /* 悬停时添加下划线 */
}
</style>