<template>
    <div>
      <h1>Boundary details</h1>
      <p><strong>filename:</strong> {{ fileName }}</p>
      <p><strong>complexity:</strong> {{ complexity }}</p>
      <div>{{ details }}</div>
      <table border="1">
        <thead>
          <tr>
            <th>Length</th>
            <th>Width</th>
            <th>Total changes</th>
            <th>Max changes</th>
            <th>Complexity</th>
          </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ details.size_length }}</td>
                <td>{{ details.size_width }}</td>
                <td>{{ details.total_changes }}</td>
                <td>{{ details.max_changes }}</td>
                <td>{{ details.complexity }}</td>
            </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
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
    },
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

  