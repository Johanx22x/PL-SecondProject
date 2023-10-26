<template>
  <el-container class="d-flex justify-content-center align-items-center flex-column m-0 p-0 home-view h-100 w-100">
    <el-text class="text-center">
      <h1>Welcome to MonchaTEC administration system!</h1>
      <h5>Here you can manage and control the restaurant</h5>
    </el-text>
    <el-button type="primary" size="large" class="mt-2">Make an order</el-button>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
});
</script>

<style>
.home-view {
  background-image: url('../assets/background.jpg');
  background-size: cover;
}
</style>
