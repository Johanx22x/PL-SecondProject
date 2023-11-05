<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-container class="d-flex flex-row justify-content-between">
                <el-text><h1>{{ dish.name }}</h1></el-text>
                <el-text><h3>$ {{ dish.foods?.reduce((acc, food) => acc + food.price, 0).toFixed(2) }}</h3></el-text>
            </el-container>
            <el-divider></el-divider>
        </el-header>
        <el-container class="w-100 h-100">
            <el-main class="m-0 p-0 w-100 h-100">
                <el-scrollbar class="w-100" style="height: 64vh;">
                    <!-- food in dish.foods -->
                    <el-card class="m-2" v-for="food in dish.foods" :key="food.id" shadow="hover">
                        <el-card-body>
                            <el-row>
                                <el-col :span="12" class="text-start">
                                    <el-text><h3>{{ food.name }}</h3></el-text>
                                </el-col>
                                <el-col :span="12">
                                    <el-text class="text-end"><h5>$ {{ food.price }}</h5></el-text>
                                </el-col>
                                <el-col :span="24">
                                    <el-text class="text-end"><h5>Calories: {{ food.calories }}</h5></el-text>
                                </el-col>
                            </el-row>
                        </el-card-body>
                    </el-card>
                </el-scrollbar>
                <el-button type="primary" class="text-decoration-none w-100 mt-5 m-0" size="large" tag="router-link" to="/orders/menu/traditional">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-arrow-left" />
                    </template>
                    Go Back 
                </el-button>
            </el-main>
        </el-container> 
    </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'; 
import Dish from '@/dish';

export default defineComponent({
  name: 'ViewDishView',
  components: {
  },
  data() {
    return {
        dish: {} as Dish,
    }
  },
  mounted() {
    this.fetchDish().then((res) => {
        this.dish = res.data;
    });
  },
  methods: {
    async fetchDish() {
        let res = await axios.get<Dish>(`/api/dish/${this.$route.params.id}`);
        return res;
    },
  }
})
</script>
