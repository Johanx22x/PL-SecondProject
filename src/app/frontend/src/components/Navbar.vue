<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    @select="handleSelect"
  >
    <el-menu-item index="0" class="m-0 p-0">
      <router-link to="/" style="text-decoration: none;" class="logo">
        <img
          class="logo"
          src="../assets/logo.png"
          alt="MonchaTEC"
        />
      </router-link>
    </el-menu-item>
    <div class="flex-grow" />
    <el-menu-item index="1">
      <router-link to="/orders" style="text-decoration: none;">Orders</router-link>
    </el-menu-item>
    <el-menu-item index="2">
      <router-link to="/invoices" style="text-decoration: none;">Invoices</router-link>
    </el-menu-item>
    <el-menu-item index="3">
      <router-link to="/statistics" style="text-decoration: none;">Statistics</router-link>
    </el-menu-item>
    <el-sub-menu index="4">
      <template #title>Administration</template>
      <router-link to="/inventory" style="text-decoration: none;">
        <el-menu-item index="4-1">Inventory</el-menu-item>
      </router-link>
      <router-link to="/dishes" style="text-decoration: none;">
        <el-menu-item index="4-2">Dishes</el-menu-item>
      </router-link>
      <router-link to="/configuration" style="text-decoration: none;">
        <el-menu-item index="4-3">Configuration</el-menu-item>
      </router-link>
    </el-sub-menu>
    <el-menu-item index="5">
      <router-link to="/about" style="text-decoration: none;">About</router-link>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Navbar',
  data() {
    return {
      activeIndex: '0',
    };
  },
  methods: {
    handleSelect(key: string) {
      console.log(key);
    },
  },
});
</script>

<style>
.flex-grow {
  flex-grow: 1;
}

.logo {
    width: 100%;
    height: 100%;
}
</style>
