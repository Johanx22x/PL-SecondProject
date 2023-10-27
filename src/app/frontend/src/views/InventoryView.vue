<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-3 text-start h-100 w-100">
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
                <li v-for="(food) in filteredItems" class="mb-3" :key="food.id">
                    <el-card shadow="hover">
                        <el-descriptions :title="food.name">
                            <el-descriptions-item label="Calories">{{ food.calories }}</el-descriptions-item>
                            <el-descriptions-item label="Price">${{ food.price }}</el-descriptions-item>
                        </el-descriptions>
                    </el-card>
                </li>
            </ul>
        </el-scrollbar>
    </el-container>
</template>
<script lang="ts">
    import { defineComponent } from "vue";
    import axios from "axios";
    import Food from "@/food";


    export default defineComponent({
        data() {
            return {
                foodItems: [] as Food[],
                filterTerm: "",
                selectedValue: null
            }
        },
        methods: {
            async fetchFoods() {
                let res = await axios.get<Food[]>("/api/food");
                return res;
            }
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
        },

    });
</script>
