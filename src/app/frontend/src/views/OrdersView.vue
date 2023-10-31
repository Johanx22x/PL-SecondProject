<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-container class="d-flex flex-row justify-content-between">
                <el-text><h1>Orders</h1></el-text>
                <el-button type="primary" class="me-3 mt-3" size="large" tag="router-link" to='/orders/add' style="text-decoration: none;">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-plus" size="xl" />
                    </template>
                    New Order 
                </el-button>
            </el-container>
            <el-divider></el-divider>
        </el-header>
      <el-container>
        <el-main class="m-0 p-0 w-100 me-5">
            <el-text class="text-start"><h3>Active</h3></el-text>
            <el-container class="w-100">
                <el-scrollbar height="70vh" class="w-100">
                    <ul class="list-inline">
                    <li v-for="(bill) in activeOrders" class="mb-3" :key="bill.id">
                        <el-card shadow="hover">
                            <el-container class="d-flex flex-row">
                                <el-container class="w-100">
                                    <el-descriptions 
                                        class="w-100"
                                        :column="2"
                                        :title="bill.id"
                                        >
                                            <el-descriptions-item label="Number of orders:" :width="200">{{ bill.ordersAmount }}</el-descriptions-item>
                                            <el-descriptions-item label="Amount:" :width="200">${{ bill.total }}</el-descriptions-item>
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3">
                                    <el-button type="danger" class="text-decoration-none mb-3 w-100" size="large" @click="cancelOrder(bill.id)">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-ban" size="xl" />
                                        </template>
                                        Cancel
                                    </el-button>
                                    <el-button type="primary" class="text-decoration-none w-100 m-0 mb-3" size="large">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-edit" size="xl" />
                                        </template>
                                        Edit 
                                    </el-button>
                                    <el-button type="success" class="text-decoration-none w-100 m-0" size="large" @click="payOrder(bill.id)">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                                        </template>
                                        Pay 
                                    </el-button>
                                </el-container>
                            </el-container>
                        </el-card>
                    </li>
                    </ul>
                </el-scrollbar>
            </el-container>
        </el-main>
        <el-aside class="m-0 p-0">
            <el-text class="text-start"><h3>Paid</h3></el-text>
            <el-container class="w-100">
                <el-scrollbar height="70vh" class="w-100">
                    <ul class="list-inline">
                    <li v-for="(bill) in paidOrders" class="mb-3" :key="bill.id">
                        <el-card shadow="hover">
                            <el-container class="d-flex flex-row">
                                <el-container class="w-100">
                                    <el-descriptions 
                                        :title="bill.id"
                                        class="w-100"
                                        :column="1"
                                        >
                                            <el-descriptions-item label="Number of orders:" :width="200">{{ bill.ordersAmount }}</el-descriptions-item>
                                            <el-descriptions-item label="Amount:" :width="200">${{ bill.total }}</el-descriptions-item>
                                            <el-descriptions-item label="Payment method:" :width="200">{{ $store.state.paymentTypes.find((type) => type.value === bill.type)?.label }}</el-descriptions-item>
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3 m-0 w-50">
                                    <el-button type="primary" class="text-decoration-none w-100 m-0" size="large" tag="router-link" :to="`/orders/view/${bill.id}`">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-eye" size="xl" />
                                        </template>
                                        View
                                    </el-button>
                                </el-container>
                            </el-container>
                        </el-card>
                    </li>
                    </ul>
                </el-scrollbar>
            </el-container>
        </el-aside>
      </el-container>
    </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios';
import Bill from '@/bill';
import { ElNotification } from 'element-plus';

export default defineComponent({
  name: 'OrdersView',
  components: {
  },
  data() {
    return {
        bills: [] as Bill[],
    }
  },
  mounted() {
    this.fetchBills().then((res) => {
        this.bills = res.data;
    });
  },
  methods: {
    async fetchBills() {
        let res = await axios.get<Bill[]>("/api/bill");
        return res;
    },
    async cancelOrder(id: number) {
        let res = await axios.delete(`/api/bill/${id}`);
        if (res.status == 200) {
            ElNotification({
                title: "Success",
                message: "Order cancelled",
                type: "success"
            });
            this.bills = this.bills.filter((bill) => {
                return bill.id != id;
            });
        } else {
            ElNotification({
                title: "Error",
                message: "Order could not be cancelled",
                type: "error"
            });
        }
    },
    async payOrder(id: number) {
        // TODO: Ask if want to pay with cash or card 
        let res = await axios.put(`/api/bill/${id}/pay`);
        if (res.status == 200) {
            ElNotification({
                title: "Success",
                message: "Order paid",
                type: "success"
            });

            this.bills = await this.fetchBills().then((res) => {
                return res.data;
            });
        } else {
            ElNotification({
                title: "Error",
                message: "Order could not be paid",
                type: "error"
            });
        }
    }
  },
  computed: {
    activeOrders(): Bill[] {
        let active = this.bills.filter((bill) => {
            return !bill.is_paid;
        });

        active.forEach(async (bill) => {
            try {
                bill.ordersAmount = await axios.get(`/api/bill/${bill.id}/orders`).then((res) => res.data.length);
            } catch (e: any) {
                ElNotification({
                    type: 'error',
                    title: 'Error loading bill order data!',
                    message: e.toString()
                });
            }
        });

        return active;
    },
    paidOrders(): Bill[] {
        let paid = this.bills.filter((bill) => {
            return bill.is_paid;
        });

        paid.forEach(async (bill) => {
            try {
                bill.ordersAmount = await axios.get(`/api/bill/${bill.id}/orders`).then((res) => res.data.length);
            } catch (e: any) {
                ElNotification({
                    type: 'error',
                    title: 'Error loading bill order data!',
                    message: e.toString()
                });
            }
        });

        return paid;
    },
  }
})
</script>
