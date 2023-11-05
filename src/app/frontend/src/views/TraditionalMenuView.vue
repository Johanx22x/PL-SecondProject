<template>
    <el-container class="container-sm d-flex flex-column mt-5">
        <el-scrollbar height="75vh">
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
                    <li v-for="(dish) in dishes" class="mb-3" :key="dish.id">
                        <el-card shadow="hover">
                            <el-container class="d-flex flex-row">
                                <el-container class="w-100">
                                    <el-descriptions 
                                        :title="dish.name" 
                                        class="w-100"
                                        :column="2"
                                        >
                                        <el-descriptions-item label="Food count:" :width="200">{{ dish.foods.length }}</el-descriptions-item>
                                        <el-descriptions-item label="Price:" :width="200">${{ dish.foods.reduce((acc, food) => acc + food.price, 0).toFixed(2) }}</el-descriptions-item>
                                        <el-descriptions-item label="Calories:" :width="200">{{ dish.foods.reduce((acc, food) => acc + food.calories, 0) }}</el-descriptions-item>
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center">
                                    <el-button type="primary" class="text-decoration-none w-100 m-0" size="large" tag="router-link" :to="'/dishes/view/' + dish.id">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-eye" />
                                        </template>
                                        View Foods
                                    </el-button>
                                    <el-button type="success" class="text-decoration-none w-100 mt-3 m-0" size="large" @click="addOrder(dish)">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-plus" />
                                        </template>
                                        Add to Order 
                                    </el-button>
                                </el-container>
                            </el-container>
                        </el-card>
                    </li>
                </el-skeleton>
            </ul>
        </el-scrollbar>
        <!-- go back button -->
        <el-button type="primary" class="text-decoration-none w-100 mt-5 m-0" size="large" tag="router-link" to="/orders/menu">
            <template #icon>
                <font-awesome-icon icon="fa-solid fa-arrow-left" />
            </template>
            Go Back 
        </el-button>
    </el-container>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import Dish from "@/dish";
    import axios from "axios";
    import { ElNotification } from "element-plus";

    export default defineComponent({
        data() {
            return {
                dishes: [] as Dish[],
                loading: true,
            }
        },
        methods: {
            async fetchDishes() {
                return await axios.get<Dish[]>("/api/dish");
            },

            addOrder(dish: Dish) {
                // @ts-ignore
                let orders = this.$store.getters.getOrders;

                // If order already in orders, increment quantity 
                // @ts-ignore
                let order = orders.find((order) => order.name === dish.name);
                if (order) {
                    order.quantity++;
                    // @ts-ignore
                    this.$store.commit("setOrders", orders);
                    ElNotification({
                        title: "Success",
                        message: "Added to order",
                        type: "success",
                    });
                    return;
                } else {
                    // @ts-ignore
                    this.$store.commit("setOrders", orders.concat({
                        id: dish.id,
                        name: dish.name,
                        price: dish.foods.reduce((acc, food) => acc + food.price, 0),
                        quantity: 1,
                    }));
                }

                ElNotification({
                    title: "Success",
                    message: "Added to order",
                    type: "success",
                });
            },
        },
        mounted() {
            this.fetchDishes().then((res) => {
                this.dishes = res.data;
            });
            this.loading = false;
        },
    });
</script>
