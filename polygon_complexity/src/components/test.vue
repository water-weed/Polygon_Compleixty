<template>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
      @header-dragend="handleDragEnd"
    >
      <el-table-column prop="fileName" label="Polygon" />
      <el-table-column prop="method1" label="Method 1" />
      <el-table-column prop="method2" label="Method 2" />
    </el-table>
  </template>
  
  <script>
  export default {
    name:"test",
    data() {
      return {
        tableData: [
          { fileName: "Polygon1", method1: 10, method2: 20 },
          { fileName: "Polygon2", method1: 15, method2: 25 },
        ],
      };
    },

    methods: {
      handleDragEnd({ oldColumnIndex, newColumnIndex }) {
        console.log("Dragged from:", oldColumnIndex, "to:", newColumnIndex);
      },
    },
  };
  </script>
  