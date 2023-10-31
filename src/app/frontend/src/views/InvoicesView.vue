<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-text><h1>Invoices</h1></el-text>
            <el-divider></el-divider>
        </el-header>
        <div class="d-flex flex-row justify-content-between w-100">
            <div class="w-100 mb-3 mt-3 d-flex">
                <el-select 
                    v-model="paymentTypeValue"
                    placeholder="Payment Type"
                    @clear="() => paymentTypeValue = null"
                    size="large"
                    clearable >
                    <el-option
                        v-for="option in $store.state.paymentTypes"
                        :key="option.value"
                        :label="option.label"
                        :value="option.value" />
                </el-select>
                <el-container class="d-flex flex-row justify-content-center align-items-center">
                    <el-input-number v-model="startPriceValue" :min="0" :step="0.1" size="large" class="ms-3" placeholder="Min Amount" clearable/>
                    <el-input-number v-model="endPriceValue" :min="0" :step="0.1" size="large" class="ms-3" placeholder="Max Amount"  clearable/>
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
                <el-skeleton :loading="loading" :count="10" animated>
                    <template #template>
                        <li class="mb-3">
                            <el-card shadow="hover">
                                <el-container class="w-100 d-flex flex-column">
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
                    <template #default>
                        <li v-for="(bill) in filteredItems" class="mb-3" :key="bill.id">
                            <el-card shadow="hover">
                                <el-container class="d-flex flex-row">
                                    <el-container class="w-100">
                                        <el-descriptions 
                                            class="w-100"
                                            :column="2"
                                            >
                                            <el-descriptions-item label="Amount" :width="200">${{ bill.total }}</el-descriptions-item>
                                            <el-descriptions-item label="Payment Type" :width="200">{{ $store.state.paymentTypes.find((type) => type.value === bill.type)?.label }}</el-descriptions-item>
                                            <el-descriptions-item label="Date" :width="200">{{ bill.date_time }}</el-descriptions-item>
                                            <el-descriptions-item label="Number of orders" :width="200">{{ bill.ordersAmount }}</el-descriptions-item>
                                        </el-descriptions>
                                    </el-container>
                                    <el-container class="d-flex flex-column justify-content-center ms-3">
                                        <el-button type="primary" class="text-decoration-none w-100 m-0" size="large" tag="router-link" :to="'/orders/view/' + bill.id">
                                            <template #icon>
                                                <font-awesome-icon icon="fa-solid fa-eye" />
                                            </template>
                                            View Orders
                                        </el-button>
                                    </el-container>
                                </el-container>
                            </el-card>
                        </li>
                    </template>
                </el-skeleton>
            </ul>
        </el-scrollbar>
    </el-container>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import axios from "axios";
    import Bill from "@/bill";
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
                shortcuts,
                loading: true
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

                    let date2 = null;
                    let date1 = null;
                    if (this.daterangeValue !== null) {
                        date2 = new Date(this.daterangeValue[1])
                        date2.setHours(23, 59, 59);
                        date1 = new Date(this.daterangeValue[0]);
                    } 

                    return (
                        (this.paymentTypeValue === null || bill.type === this.paymentTypeValue) &&
                        // @ts-ignore
                        (((date1 === null) && (date2 === null)) || ((date >= date1) && date <= date2)) &&
                        (this.startPriceValue === null || bill.total >= this.startPriceValue) &&
                        (this.endPriceValue === null || bill.total <= this.endPriceValue)
                    )
                });
            },
        },
        async mounted() {
            let bills = await this.fetchBills();
            this.billItems = bills.data;

            this.billItems.forEach(async (bill) => {
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

            this.loading = false;
        },

    });
</script>
