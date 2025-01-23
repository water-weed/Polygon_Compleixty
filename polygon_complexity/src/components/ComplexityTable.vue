<template>
    <div>
      <h2>Complexity</h2>
  
      <!-- 选择列 -->
      <div class="column-selector">
        <el-checkbox-group v-model="selectedColumns">
          <el-checkbox 
          v-for="col in allColumns" 
          :key="col.key" 
          :label="col.key">
            {{ col.label }}
          </el-checkbox>
        </el-checkbox-group>
      </div>
  
      <!-- 表格 -->
      <el-table :data="sortedData" style="width: 100%" border>
        <!-- 第一列：Polygon Name -->
        <el-table-column 
          label="Polygon" 
          prop="fileName" 
          v-if="isColumnVisible('fileName')" 
        >
        </el-table-column>
  
        <!-- 第二列：图片 -->
        <el-table-column label="Image" v-if="isColumnVisible('image')">
          <template #default="{ row }">
            <img :src="row.url" alt="Polygon Image" width="100" />
          </template>
        </el-table-column>
  
        <!-- 可拖动方法列 -->
        <draggable v-model="columns" tag="template" item-key="key" handle=".drag-handle">
          <template #item="{ element }">
            <el-table-column
              v-if="isColumnVisible(element.key)"
              :key="element.key"
              :label="element.label"
              :prop="element.key"
              sortable
            >
              <template #header>
                <span class="drag-handle">⬍</span> {{ element.label }}
              </template>
  
              <template #default="{ row }">
                <a href="#" @click.prevent="navigateWithDetails(row, element.key)">
                  {{ getTotalComplexity(row.data, element.key) }}
                </a>
              </template>
            </el-table-column>
          </template>
        </draggable>
      </el-table>
    </div>
  </template>
  
  <script>
  import draggable from "vuedraggable";
  
  export default {
    name: "ComplexityTable",
    components: { draggable },
    props: {
      data: Array,
      urls: Object,
    },
    data() {
      return {
        currentSortMethod: null,
        sortAscending: true,
        selectedColumns: [], // 用户选择的列
        columns: [], // 可拖动列顺序
      };
    },

    computed: {
      methods() {
        if (this.data && this.data.length > 0) {
          const firstFileData = this.data[0];
          const fileName = Object.keys(firstFileData)[0];
          if (firstFileData[fileName] && typeof firstFileData[fileName] === "object") {
            return Object.keys(firstFileData[fileName]);
          }
        }
        return [];
      },

      allColumns() {
        return [
          { key: "fileName", label: "Polygon" },
          { key: "image", label: "Image" },
          ...this.methods.map((method) => ({ key: method, label: method })),
        ];
      },

      sortedData() {
        if (!Array.isArray(this.data) || this.data.length === 0) {
          return [];
        }
  
        const polygons = this.data.map((item) => {
          const fileName = Object.keys(item)[0];
          const data = item[fileName];
          const url = this.urls[fileName];
          return { fileName, data, url };
        });
  
        if (!this.currentSortMethod) {
          return polygons;
        }
  
        return [...polygons].sort((a, b) => {
          const complexityA = this.getTotalComplexity(a.data, this.currentSortMethod);
          const complexityB = this.getTotalComplexity(b.data, this.currentSortMethod);
          return this.sortAscending ? complexityA - complexityB : complexityB - complexityA;
        });
      },
    },

    watch: {
      methods(newMethods) {
        this.columns = this.allColumns;
        this.selectedColumns = this.allColumns.map((col) => col.key);
      },
    },

    methods: {

      getTotalComplexity(complexityData, method) {
        return (parseFloat(complexityData[method]?.complexity) || 0).toFixed(4);
      },

      sortTable(method) {
        if (this.currentSortMethod === method) {
          this.sortAscending = !this.sortAscending;
        } else {
          this.currentSortMethod = method;
          this.sortAscending = true;
        }
      },

      isColumnVisible(key) {
        return this.selectedColumns.includes(key);
      },

      navigateWithDetails(polygon, method) {
        const routeMap = {
          DownsamplingBoundary: { routeName: "DownsamplingBoundaryDetails" },
          DownsamplingArea: { routeName: "DownsamplingAreaDetails" },
          Boundary: { routeName: "BoundaryDetails" },
          Triangulation: { routeName: "TriangulationDetails" },
          Entropy: { routeName: "EntropyDetails" },
          Mat: { routeName: "MatDetails" },
          Edf: { routeName: "EdfDetails" },
          Weighted: { routeName: "WeightedDetails" },
        };
  
        const targetRoute = routeMap[method];
  
        if (!targetRoute) {
          console.error(`Unknown method: ${method}`);
          return;
        }
  
        this.$store.commit("setDetails", polygon.data[method]);
  
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
    },
  };
  </script>
  
  <style scoped>
  /* 选择列样式 */
  .column-selector {
    margin-bottom: 10px;
  }
  
  /* 表格样式 */
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th,
  td {
    padding: 8px 12px;
    border: 1px solid #ddd;
    text-align: center;
  }
  
  /* 表头 */
  th {
    cursor: pointer;
    background-color: #f2f2f2;
  }
  
  /* 拖动手柄 */
  .drag-handle {
    cursor: grab;
    margin-right: 5px;
  }
  </style>
  