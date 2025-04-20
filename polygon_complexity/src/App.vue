<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
/* global style */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
