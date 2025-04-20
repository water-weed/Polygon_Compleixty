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

      <!-- table -->
      <el-table
        :data="sortedData"
        border
        style="width: 100%"
        v-if="sortedData.length"
        :key="tableKey"
        :fit = "true"
      >

        <!-- Fixed polygon column -->
        <el-table-column prop="fileName" label="Polygon"/>
  
        <!-- Fixed image column -->
        <el-table-column label="Image">
          <template #default="scope">
            <img :src="scope.row.url" alt="Polygon Image" style="max-width: 100%; height: auto; display: block;" />
          </template>
        </el-table-column>
  
        <!-- dynamically generated column -->
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
import preload1Img from '../assets/preload_images/preload1.jpg';
import preload2Img from '../assets/preload_images/preload2.jpg';
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
        visibleMethods: [], // visible column
        sortKey: "", // current order key
        sortOrder: 1, // sorting order: 1 for ascending, -1 for descending
        tableKey: 0,
        displayData: [], 
        displayUrls:{},
        fileUrl:null,
        /*initialData: [ 
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
      // initialize visibleMethods after the component is mounted
      //console.log("methods:", this.methods);
      axios.get('http://localhost:5000/api/complexity').then(
        response =>{
          const rawData = response.data.data;
          //console.log(rawData);
  
          // convert the object returned by the backend into an array format
          const polygonData = Object.keys(rawData).map(fileName => {
            return { [fileName]: rawData[fileName] };
          });
          this.initialData = polygonData;
          this.displayData = [...this.initialData]; // populate the table with initial data
          this.displayUrls = { ...this.initialUrls };
          this.visibleMethods = this.methods;

          this.$nextTick(() => {
            this.initSortable(); // ensure drag initialization is executed after DOM rendering is completed
            });
        }
      )
      //this.displayData = [...this.initialData]; 
      //this.displayUrls = { ...this.initialUrls };
      //this.visibleMethods = this.methods;
      //console.log(this.visibleMethods);
    },

    watch: {
    // monitor changes in table data
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
        // re-rendering after the order of the header changes
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
          // check if the data array exists and contain at least one file
          if (this.displayData && this.displayData.length > 0) {
            //console.log(this.data);
            const firstFileData = this.displayData[0];
            const fileName = Object.keys(firstFileData)[0]; // get filename:file0, file1
            // check if the file name and polygon data exist
            if (firstFileData[fileName] && typeof firstFileData[fileName] === 'object') {
              const samplePolygon = firstFileData[fileName]; // get the information of the first polygon
              return Object.keys(samplePolygon); // return all measures name 
              }
            }
            return []; // if there is no valid data, an empty array is returned
          },

      // sorted data
      sortedData() {
        if (!Array.isArray(this.displayData) || this.displayData.length === 0) {
          return []; // if this.data is invalid, return an empty array to avoid errors
        }

        const polygons = this.displayData.map(item => {
          const fileName = Object.keys(item)[0]; // extract file number
          const data = item[fileName]; // extract complexity value
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
      // get complexity
      getTotalComplexity(data, method) {
        //console.log(data);
        //console.log(method),
        //console.log(data[method].complexity);
        return (parseFloat(data[method].complexity ?? 0)).toFixed(4); // if there is no value, return 0
      },

      // sorting
      handleSortChange({ prop, order }) {
        this.sortKey = prop;
        this.sortOrder = order === "ascending" ? 1 : -1;
      },

      addDataToTable(newData) {
        //console.log('Adding new data to table:', newData);
        //this.displayData = this.displayData.concat(newData);
        this.displayData = [...this.initialData,...newData];
        this.displayUrls = {
          ...this.initialUrls, // keep current Urls
          ...this.urls, // add or renew URLs
        };
        console.log('Updated displayData:', this.displayData);
        console.log(this.urls);
        console.log(this.displayUrls);
      },

      // the operation of clicking complexity value
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

    //Export data
    async handleExport() {
        const workbook = new ExcelJS.Workbook();
        const sheet = workbook.addWorksheet("Table Data");
        
        // 
        sheet.addRow(["Polygon", "Image", ...this.visibleMethods]);
        
        // set up table header
        for (let i = 0; i < this.sortedData.length; i++) {
            const row = this.sortedData[i];
            const newRow = [row.fileName, "", ...this.visibleMethods.map((method) => row.data[method].complexity ?? "")];
            sheet.addRow(newRow);
            
            // embed image
            const imageResponse = await axios.get(row.url, { responseType: "arraybuffer" });
            const imageId = workbook.addImage({
                buffer: imageResponse.data,
                extension: "png",
            });
            
            sheet.addImage(imageId, {
                tl: { col: 1, row: i + 1 }, 
                ext: { width: 50, height: 50 }, 
            });
        }
        
        // export file
        const buffer = await workbook.xlsx.writeBuffer();
        const blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
       
        if (this.fileUrl) {
          URL.revokeObjectURL(this.fileUrl); //clear oled Blob URL
        }
        this.fileUrl = URL.createObjectURL(blob); // generate new Blob URL
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

          //const movedMethod = this.visibleMethods.splice(oldIndex, 1)[0];
          //this.visibleMethods.splice(newIndex, 0, movedMethod);

          //console.log("After change:", this.visibleMethods);

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
/* change color of checkbox*/
:deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: rgb(100, 53, 0); /* change the color of selected word */
  font-size: 19px;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: rgb(100, 53, 0); /* change color of selected background */
  border-color: rgb(100, 53, 0); /* change color of selected border */
}

:deep(.el-checkbox__input:not(.is-checked) + .el-checkbox__label) {
  color: #a5c2be; /* set the color of unselected word */
  font-size: 19px;
}

:deep(.el-checkbox__inner) {
  border-color: #a5c2be; /* set the color of unselected border */
}

:deep(.el-table) {
  font-size: 14px; /* set table font size*/
}

/* table header font color */
:deep(.el-table__header-wrapper th) {
  color: #a5c2be; 
}

/* table content font color */
:deep(.el-table__body-wrapper td) {
  color: rgb(100, 53, 0); 
}

/* table link color */
:deep(.el-table__body-wrapper a) {
  color: rgb(100, 53, 0); /* default color */
  text-decoration: none; /* remove underline */
}

/* table link hover color */
:deep(.el-table__body-wrapper a:hover) {
  color: #fdca6b;; /* color when hover */
  text-decoration: underline; /* underline when hover */
}
</style>