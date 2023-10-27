<template>
    <el-container class="container-sm d-flex flex-column">
        <div class="d-flex flex-row justify-content-between w-100">
            <div class="w-100 mb-3 mt-3 d-flex">
                <el-input size="large" type="text" class="h-100 w-50" placeholder="Filter" v-model="filterTerm"></el-input>
                <el-select class="h-100">
                    <el-option>Semen</el-option>
                </el-select>
            </div>
            <div class="mt-3 mb-3 d-flex h-100">
                <el-button type="primary" class="h-100"><font-awesome-icon icon="fa-solid fa-plus" class="me-3" size="xl" />New Food</el-button>
            </div>
        </div>
        <el-scrollbar height="80vh">
            <ul class="list-inline">
                <li v-for="(food) in filteredItems" class="mb-3" :key="food.id">
                    <el-card shadow="hover">
                        <template #header>{{food.name}}</template>
                        <!-- <el-descriptions :title="food.name" border direction="vertical">
                            <el-descriptions-item label="Name">{{ food.name }}</el-descriptions-item>
                            <el-descriptions-item label="Calories">{{ food.calories }}</el-descriptions-item>
                            <el-descriptions-item label="Price">${{ food.price }}</el-descriptions-item>
                            <el-descriptions-item label="Type">{{ food.type }}</el-descriptions-item>
                            <el-descriptions-item label="SubType">{{ food.subtype }}</el-descriptions-item>
                        </el-descriptions> -->
                    </el-card>
                </li>
            </ul>
        </el-scrollbar>
    </el-container>
</template>
<script lang="ts">
    import { defineComponent } from "vue";
    import axios from "axios";

    interface Food {
        id: number
        calories: number,
        name: string,
        price: number,
        type: number,
        subtype: number
    };

    export default defineComponent({
        data() {
            return {
                foodItems: [] as Food[],
                filterTerm: ""
            }
        },
        methods: {
            async fetchFoods() {
                let res = await axios.get<Food[]>("/api/food");
                return res;
            }
        },
        computed: {
            filteredItems() {
                return this.foodItems.filter((item: Food) => item.name.toLowerCase().includes(this.filterTerm.toLowerCase()));
            }
        },
        async mounted() {
            let foods = await this.fetchFoods();
            this.foodItems = foods.data;
        },

    });
</script>
