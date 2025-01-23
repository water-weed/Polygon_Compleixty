<template>
    <div>
      <h1>Weighted details</h1>
      <p><strong>filename:</strong> {{ fileName }}</p>
      <p><strong>complexity:</strong> {{ complexity }}</p>
      <div>{{ details }}</div>
      <table border="1">
        <thead>
          <tr>
            <th>Frequency of the vibration</th>
            <th>Amplitude of the vibration</th>
            <th>Deviation from the convex hull</th>
            <th>Complexity</th>
          </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ details.ampl }}</td>
                <td>{{ details.conv }}</td>
                <td>{{ details.freq }}</td>
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

  