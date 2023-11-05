<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-text><h1>{{ order.name }}</h1></el-text>
            <el-divider></el-divider>
        </el-header>
        <el-container class="w-100 h-100">
            <el-main class="m-0 p-0 w-100 h-100 text-start">
                <el-text><h3>Date:</h3><h5>{{ order.date_time }}</h5></el-text>
                <el-text><h3 class="mt-3">Total:</h3><h5>$ {{ order.total }}</h5></el-text>
                <el-text><h3 class="mt-3">Dishes:</h3></el-text>
                <el-scrollbar class="w-100" style="height: 45vh;">
                    <!-- food in dish.foods -->
                    <el-card class="mb-2" v-for="dish in orders" :key="dish.id" shadow="hover">
                        <el-card-body>
                            <el-row>
                                <el-col :span="12" class="text-start">
                                    <el-text><h5>{{ dish.name }}</h5></el-text>
                                </el-col>
                            </el-row>
                        </el-card-body>
                    </el-card>
                </el-scrollbar>
                <el-button type="primary" class="text-decoration-none w-100 mt-5 m-0" size="large" tag="router-link" to="/orders">
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

export default defineComponent({
  name: 'ViewOrderView',
  components: {
  },
  data() {
    return {
        order: {},
        orders: [],
    }
  },
  mounted() {
    this.fetchOrder().then((res) => {
        this.order = res.data;
    });

    this.fetchOrders().then((res) => {
        // @ts-ignore
        let orders = res.data.filter((dish) => dish.bill_id === Number(this.$route.params.id));
        
        // @ts-ignore
        orders.forEach((order) => {
            // @ts-ignore
            order.dishes.forEach((dish) => {
                // @ts-ignore
                this.orders.push(dish);
            });
        });
    });
  },
  methods: {
    async fetchOrder() {
        let res = await axios.get(`/api/bill/${this.$route.params.id}`);
        return res;
    },
    async fetchOrders() {
        let res = await axios.get(`/api/order/`);
        return res
    },
  }
})
</script>
