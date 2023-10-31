<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-text><h1>Dishes</h1></el-text>
            <el-divider></el-divider>
        </el-header>
        <div class="d-flex flex-row justify-content-between w-100">
            <div class="w-100 mb-3 mt-3 d-flex">
                <el-input size="large" type="text" class="h-100 w-25 me-3" placeholder="Name" v-model="dishName" />
            </div>
            <div class="mt-3 mb-3 d-flex h-100">
                <el-button type="primary" class="h-100 text-decoration-none" size="large" tag="router-link" to='/dishes/add'>
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-plus" class="me-3" size="xl" />
                    </template>
                    New Dish
                </el-button>
            </div>
        </div>
        <el-scrollbar height="70vh">
            <ul class="list-inline">
                <el-skeleton :loading="loading" :count="10" animated>
                    <template #template>
                        <li class="mb-3">
                            <el-card shadow="hover">
                                <el-container class="d-flex w-100 flex-column">
                                    <el-skeleton-item variant="h3" style="width: 10%;" class="mb-3"></el-skeleton-item>
                                    <el-skeleton-item variant="text" class="w-100 mb-3"></el-skeleton-item>
                                    <el-skeleton-item variant="text" class="w-75 mb-3"></el-skeleton-item>
                                    <el-skeleton-item variant="text" class="w-25"></el-skeleton-item>
                                </el-container>
                            </el-card>
                        </li>
                        <li class="mb-3">
                            <el-card shadow="hover">
                                <el-container class="w-100 d-flex flex-column">
                                    <el-skeleton-item variant="h3" style="width: 15%;" class="mb-3"></el-skeleton-item>
                                    <el-skeleton-item variant="text" class="w-50 mb-3"></el-skeleton-item>
                                    <el-skeleton-item variant="text" class="w-25 mb-3"></el-skeleton-item>
                                    <el-skeleton-item variant="text" class="w-75"></el-skeleton-item>
                                </el-container>
                            </el-card>
                        </li>
                    </template>
                    <li v-for="(dish, idx) in filteredItems" class="mb-3" :key="dish.id">
                        <el-card shadow="hover">
                            <el-container class="d-flex flex-row">
                                <el-container class="w-100">
                                    <el-descriptions 
                                        :title="dish.name" 
                                        class="w-100"
                                        :column="2"
                                        >
                                        <el-descriptions-item label="Food amount:" :width="200">{{ dish.foods.length }}</el-descriptions-item>
                                        <el-descriptions-item label="Price:" :width="200">${{ dish.foods.reduce((acc, food) => acc + food.price, 0).toFixed(2) }}</el-descriptions-item>
                                        <el-descriptions-item label="Calories:" :width="200">{{ dish.foods.reduce((acc, food) => acc + food.calories, 0) }}</el-descriptions-item>
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3">
                                    <el-button type="danger" class="text-decoration-none mb-3 w-100" size="large" @click="this.delete(dish.id, idx)">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-trash" size="xl" />
                                        </template>
                                        Delete 
                                    </el-button>
                                    <el-button type="primary" class="text-decoration-none w-100 m-0" size="large" tag="router-link" :to="`/dishes/edit/${dish.id}`">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-edit" size="xl" />
                                        </template>
                                        Edit 
                                    </el-button>
                                </el-container>
                            </el-container>
                        </el-card>
                    </li>
                </el-skeleton>
            </ul>
        </el-scrollbar>
    </el-container>
</template>
<script lang="ts">
    import { defineComponent } from "vue";
    import { ElNotification } from "element-plus";
    import Dish from "@/dish";
    import axios from "axios";

    export default defineComponent({
        data() {
            return {
                loading: true,
                dishes: [] as Dish[],
                dishName: "",
            }
        },
        computed: {
            filteredItems(): Dish[] {
                this.dishes;
                return this.dishes.filter((dish: Dish) => dish.name.toLowerCase().includes(this.dishName.toLowerCase()));
            }
        },
        methods: {
            async loadDishes() {
                return await axios.get<Dish[]>("/api/dish");
            },
            async delete(id: number, idx: number) {
                let result = await axios.delete(`/api/dish/${id}`);
                if (result.status !== 200) {
                    ElNotification({
                        type: 'error',
                        title: "Couldn't delete that dish",
                        message: `Got status code ${result.status}`
                    });
                } else {
                    ElNotification({
                        type: 'success',
                        title: 'Dish deleted successfully',
                        message: 'The dish has been deleted'
                    });
                    this.dishes.splice(idx, 1);
                }
            }
        },
        async mounted() {
            let res = await this.loadDishes();
            if (res.status !== 200) {
                ElNotification({
                    type: "error",
                    title: "Error while loading dishes!",
                    message: "An error occurred while loading dishes"
                });
            } else {
                this.dishes = res.data.filter((dish: Dish) => dish.predef);
                this.loading = false;
            }
        }
    });
</script>
