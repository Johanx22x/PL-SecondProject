<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-text><h1>Invoices</h1></el-text>
            <el-divider></el-divider>
        </el-header>
        <div class="d-flex flex-row justify-content-between w-100">
            <div class="w-100 mb-3 mt-3 d-flex">
                <el-cascader
                    v-model="paymentTypeValue"
                    :placeholder="'Payment Type'"
                    :options="$store.state.paymentTypes"
                    size="large"
                    :props="{ expandTrigger: 'hover' }"
                    clearable />
                <el-container class="d-flex flex-row justify-content-center align-items-center">
                    <el-input-number v-model="startPriceValue" :min="0" :step="0.1" size="large" class="ms-3" placeholder="Min Amount" />
                    <el-input-number v-model="endPriceValue" :min="0" :step="0.1" size="large" class="ms-3" placeholder="Max Amount" />
                </el-container>
                <el-date-picker
                    v-model="daterangeValue"
                    type="daterange"
                    unlink-panels
                    range-separator="To"
                    start-placeholder="Start date"
                    end-placeholder="End date"
                    :shortcuts="shortcuts"
                    class="ms-3 h-100 w-20"
                  />
            </div>
            <div class="mt-3 mb-3 d-flex h-100">
            </div>
        </div>
        <el-scrollbar height="70vh">
            <ul class="list-inline">
                <li v-for="(bill) in filteredItems" class="mb-3" :key="bill.id">
                    <el-card shadow="hover">
                        <el-container class="d-flex flex-row">
                            <el-container class="w-100">
                                <el-descriptions 
                                    class="w-100"
                                    column="2"
                                    >
                                    <el-descriptions-item label="Amount:" :width="200">${{ bill.total }}</el-descriptions-item>
                                    <el-descriptions-item label="Payment Type:" :width="200">{{ $store.state.paymentTypes.find((type) => type.value === bill.type)?.label }}</el-descriptions-item>
                                    <el-descriptions-item label="Date:" :width="200">{{ bill.date_time }}</el-descriptions-item>
                                    <el-descriptions-item label="Orders Amount:" :width="200">{{ bill.ordersAmount }}</el-descriptions-item>
                                </el-descriptions>
                            </el-container>
                            <el-container class="d-flex flex-column justify-content-center ms-3">
                                <el-button type="primary" class="text-decoration-none w-100 m-0" size="large" tag="router-link" :to="'/orders/bill/' + bill.id">
                                    <template #icon>
                                        <font-awesome-icon icon="fa-solid fa-eye" />
                                    </template>
                                    View Orders
                                </el-button>
                            </el-container>
                        </el-container>
                    </el-card>
                </li>
            </ul>
        </el-scrollbar>
    </el-container>
</template>
<script lang="ts">
    import { defineComponent } from "vue";
    import axios from "axios";
    import Bill from "@/models/Bill";
    import { ElNotification } from "element-plus";

    const shortcuts = [
      {
        text: 'This month',
        value: [new Date(), new Date()],
      },
      {
        text: 'This year',
        value: () => {
          const end = new Date()
          const start = new Date(new Date().getFullYear(), 0)
          return [start, end]
        },
      },
      {
        text: 'Last 6 months',
        value: () => {
          const end = new Date()
          const start = new Date()
          start.setMonth(start.getMonth() - 6)
          return [start, end]
        },
      },
    ]

    export default defineComponent({
        data() {
            return {
                billItems: [] as Bill[],
                paymentTypeValue: null,
                daterangeValue: null,
                startPriceValue: null,
                endPriceValue: null,
                shortcuts
            }
        },
        methods: {
            async fetchBills() {
                let res = await axios.get<Bill[]>("/api/bill");
                return res;
            },
        },
        computed: {
            filteredItems(): Bill[] {
                return this.billItems.filter((bill) => {
                    let date = new Date(bill.date_time);
                    return (
                        (!this.paymentTypeValue || bill.type == this.paymentTypeValue) &&
                        (!this.daterangeValue || (date >= new Date(this.daterangeValue[0]) && date <= new Date(this.daterangeValue[1]).setHours(23, 59, 59))) &&
                        (!this.startPriceValue || bill.total >= this.startPriceValue) &&
                        (!this.endPriceValue || bill.total <= this.endPriceValue)
                    );
                });
            },
        },
        async mounted() {
            let bills = await this.fetchBills();
            this.billItems = bills.data;

            this.billItems.forEach(async (bill) => {
                try {
                    bill.ordersAmount = await axios.get(`/api/bill/${bill.id}/orders`).then((res) => res.data.length);
                } catch (e) {
                    0;
                }
            });
        },

    });
</script>