<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-text><h1>Inventory</h1></el-text>
            <el-divider></el-divider>
        </el-header>
        <div class="d-flex flex-row justify-content-between w-100">
            <div class="w-100 mb-3 mt-3 d-flex">
                <el-input size="large" type="text" class="h-100 w-25 me-3" placeholder="Name" v-model="filterTerm" />
                <el-cascader
                    v-model="selectedValue"
                    :options="$store.state.foodTypes"
                    size="large"
                    :props="{ expandTrigger: 'hover' }"
                    clearable />
            </div>
            <div class="mt-3 mb-3 d-flex h-100">
                <el-button type="primary" class="h-100 text-decoration-none" size="large" tag="router-link" to='/inventory/add'>
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-plus" class="me-3" size="xl" />
                    </template>
                    New Food
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
                    <li v-for="(food) in filteredItems" class="mb-3" :key="food.id">
                        <el-card shadow="hover">
                            <el-container class="d-flex flex-row">
                                <el-container class="w-100">
                                    <el-descriptions 
                                        :title="food.name" 
                                        class="w-100"
                                        :column="2"
                                        >
                                        <el-descriptions-item label="Calories:" :width="200">{{ food.calories }}</el-descriptions-item>
                                        <el-descriptions-item label="Price:" :width="200">${{ food.price }}</el-descriptions-item>
                                        <el-descriptions-item label="Category:">{{ $store.state.foodTypes.find((item) => item.value === food.type)?.label }} > {{ $store.state.foodTypes.find((item) => item.value === food.type)?.children?.find((item) => item.value === food.subtype)?.label }}</el-descriptions-item>
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3">
                                    <el-button type="danger" class="text-decoration-none mb-3 w-100" size="large" @click="this.delete(food.id)">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-trash" size="xl" />
                                        </template>
                                        Delete 
                                    </el-button>
                                    <el-button type="primary" class="text-decoration-none w-100 m-0" size="large" tag="router-link" :to="'/inventory/edit/' + food.id">
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
    import axios from "axios";
    import Food from "@/food";
    import { ElNotification } from "element-plus";


    export default defineComponent({
        data() {
            return {
                foodItems: [] as Food[],
                filterTerm: "",
                selectedValue: null,
                loading: true
            }
        },
        methods: {
            async fetchFoods() {
                let res = await axios.get<Food[]>("/api/food");
                return res;
            },

            async deleteFood(id: number) {
                return await axios.delete("/api/food/" + id + "/delete");
            },

            delete(id: number) {
                this.deleteFood(id).then(() => {
                    ElNotification({
                        title: "Success",
                        message: "Food deleted successfully",
                        type: "success"
                    });
                    this.foodItems = this.foodItems.filter((item: Food) => item.id !== id);
                }).catch(() => {
                    ElNotification({
                        title: "Error",
                        message: "Food could not be deleted, it may be in use by a dish",
                        type: "error"
                    });
                });
            },
        },
        computed: {
            filteredItems(): Food[] {
                return this.foodItems.filter(
                    (item: Food) => (
                        this.selectedValue === null || (
                            this.selectedValue[0] === item.type && this.selectedValue[1] === item.subtype)
                        ) && item.name.toLowerCase().includes(this.filterTerm.toLowerCase()));
            }
        },
        async mounted() {
            let foods = await this.fetchFoods();
            this.foodItems = foods.data;
            this.loading = false;
        },

    });
</script>
