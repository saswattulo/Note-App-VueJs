<template>
  <div id="app">
    <NavBar />
    <router-view class="content" />
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
</script>

<style>
#app {
  width: 100vw;
  min-height: 100vh;
  overflow-x: hidden;
}

.content {
  padding: 20px;
  /* Remove any default margins that might cause horizontal scroll */
  margin: 0;
  width: 100%;
  box-sizing: border-box;
}
</style>
