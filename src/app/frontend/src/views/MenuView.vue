<template>
    <el-container class="mt-5 w-100 d-flex flex-column align-items-center">
        <el-container class="d-flex flex-row justify-content-around">
            <router-link to="/orders/menu/traditional" class="text-decoration-none w-100 h-100">
            <el-card class="me-2 h-50" shadow="hover">
                <img
                src="https://takethemameal.com/files_images_v2/stam.jpg"
                class="image"
                />
                <div style="padding: 14px">
                    <h3>Traditional dishes</h3>
                </div>
            </el-card>
            </router-link>

            <router-link to="/orders/menu/healthy" class="text-decoration-none w-100 h-100">
            <el-card class="ms-2 h-50" shadow="hover">
                <img
                src="https://www.eatingwell.com/thmb/YxkWBfh2AvNYrDKoHukRdmRvD5U=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/article_291139_the-top-10-healthiest-foods-for-kids_-02-4b745e57928c4786a61b47d8ba920058.jpg"
                class="image"
                />
                <div style="padding: 14px">
                    <h3>Healthy dishes generator</h3>
                </div>
            </el-card>
            </router-link>
        </el-container>
        <el-container class="d-flex flex-row justify-content-around">
            <el-button type="danger" size="large" class="mt-2" tag="router-link" to="/orders/add" style="text-decoration: none;">
                <template #icon>
                    <font-awesome-icon icon="fa-solid fa-xmark" size="xl" />
                </template>
                Cancel
            </el-button>
        </el-container>
    </el-container>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MenuView',
});
</script>

<style>
.image {
  width: 400px;
  height: 400px;
  object-fit: cover;
}
</style>
