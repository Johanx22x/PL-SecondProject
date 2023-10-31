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
                                        >
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3">
                                    <el-button type="danger" class="text-decoration-none mb-3 w-100" size="large">
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
                                    <el-button type="success" class="text-decoration-none w-100 m-0" size="large">
                                        <template #icon>
                                            <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                                        </template>
                                        Pay 
                                    </el-button>
                                </el-container>
                            </el-container>
                        </el-card>
                    </li>
                    <li v-for="(bill) in activeOrders" class="mb-3" :key="bill.id">
                        <el-card shadow="hover">
                            <el-container class="d-flex flex-row">
                                <el-container class="w-100">
                                    <el-descriptions 
                                        class="w-100"
                                        :column="2"
                                        >
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3">
                                    <el-button type="danger" class="text-decoration-none mb-3 w-100" size="large">
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
                                    <el-button type="success" class="text-decoration-none w-100 m-0" size="large">
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
                                        :column="2"
                                        >
                                    </el-descriptions>
                                </el-container>
                                <el-container class="d-flex flex-column justify-content-center ms-3">
                                    <el-button type="success" class="text-decoration-none w-100 m-0" size="large">
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
  },
  computed: {
    activeOrders(): Bill[] {
        return this.bills.filter((bill) => {
            return !bill.is_paid;
        });
    },
    paidOrders(): Bill[] {
        return this.bills.filter((bill) => {
            return bill.is_paid;
        });
    },
  }
})
</script>
