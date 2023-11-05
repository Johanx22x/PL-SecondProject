<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Create New Order</h3>
                </el-text>
            </template>
            <el-form :model="$store.state.order" ref="formRef" :rules="formRules" label-position="top">
                <el-form-item label="Name" for="name" prop="name">
                    <el-input size="large" name="name" v-model="name" />
                </el-form-item>
                <div class="d-flex flex-row justify-content-between">
                    <el-form-item label="Table" for="table" prop="table">
                        <el-select size="large" name="table" v-model="table">
                            <el-option
                                v-for="table in tables"
                                :key="table.id"
                                :label="table.name"
                                :value="table.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Type" for="type" prop="type">
                        <el-select size="large" name="type" v-model="type">
                            <el-option
                                v-for="type in types"
                                :key="type.id"
                                :label="type.name"
                                :value="type.id"
                            />
                        </el-select>
                    </el-form-item>
                </div>
                <el-form-item label="Orders" for="orders" prop="orders">
                    <!-- Table -->
                    <el-table :data="orders" style="width: 100%">
                        <el-table-column prop="name" label="Name" />
                        <el-table-column prop="price" label="Price" />
                        <el-table-column prop="quantity" label="Quantity" />
                        <el-table-column label="Actions">
                            <template #default="{ row }">
                                <el-button type="danger" size="small" @click="removeOrder(row)">
                                    <template #icon>
                                        <font-awesome-icon icon="fa-solid fa-trash" />
                                    </template>
                                    Remove
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-button type="primary" size="large" @click="addOrder()" class="mt-3">
                        <template #icon>
                            <font-awesome-icon icon="fa-solid fa-plus" size="xl" />
                        </template>
                        Add Order 
                    </el-button>
                </el-form-item>
            </el-form>
            <el-text><h5>Total: ${{ orders.reduce((acc, order) => acc + order.price * order.quantity, 0).toFixed(2) }}</h5></el-text>
            <div class="d-flex flex-row justify-content-around mt-4">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Submit
                </el-button>
                <el-button type="primary" class="text-decoration-none" size="large" @click="$store.commit('clearOrder')">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-eraser" size="xl" />
                    </template>
                    Clear
                </el-button>
                <el-button type="danger" class="text-decoration-none" size="large" @click="goBack()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-xmark" size="xl" />
                    </template>
                    Cancel
                </el-button>
            </div>
        </el-card>
    </el-container>
</template>
<script lang="ts">
    import { defineComponent } from "vue";
    import type { FormInstance } from "element-plus";
    import { ElNotification } from "element-plus";
    import axios from "axios";
    import Table from "@/table";

    export default defineComponent({
        methods: {
            addOrder() {
                this.$router.push('/orders/menu');
            },
            async fetchTables() {
                let res = await axios.get('/api/table')
                return res.data
            },
            submit() {
                (this.$refs["formRef"] as FormInstance).validate((valid: boolean, _) => {
                    if (valid) {
                        this.formWasValid();
                        // @ts-ignore
                        this.$store.commit("clearOrder");
                    } else {
                        this.formWasInvalid();
                    }
                });
            },
            goBack() {
                // @ts-ignore
                this.$store.commit("clearOrder");

                this.$router.push('/orders');
            },
            async formWasValid() {
                // @ts-ignore
                let order = {
                    // @ts-ignore
                    name: this.$store.getters.getName,
                    // @ts-ignore
                    total: this.$store.getters.getOrders.reduce((acc, order) => acc + order.price * order.quantity, 0).toFixed(2),
                    date_time: new Date().toISOString().slice(0, 19).replace('T', ' '),
                    // @ts-ignore
                    type: this.$store.getters.getType,
                    // @ts-ignore
                    table_id: this.$store.getters.getTable,
                };

                // @ts-ignore
                let dishes = this.$store.getters.getOrders;

                let bill = null;
                try {
                    bill = await axios.post("/api/bill", order);
                } catch (error) {
                    ElNotification({
                        type: 'error',
                        title: 'Error!',
                        message: "Something went wrong!"
                    });
                    return
                }

                try {
                    await axios.post("/api/order", {bill_id: bill.data.id, dishes: dishes});
                } catch (error) {
                    ElNotification({
                        type: 'error',
                        title: 'Error!',
                        message: "Something went wrong!"
                    });
                    return
                }

                ElNotification({
                    type: 'success',
                    title: 'Success!',
                    message: 'Order was successfully submitted!'
                });

                // @ts-ignore
                this.$store.commit('clearOrder')
                this.$router.push('/orders');
            },
            formWasInvalid() {
                ElNotification({
                    type: 'error',
                    title: 'Error!',
                    message: 'One or more fields are invalid!'
                });
            },
            removeOrder(order: { name: string, price: number, quantity: number }) {
                // @ts-ignore
                let orders = this.$store.getters.getOrders;

                // If order already in orders, increment quantity 
                // @ts-ignore
                let index = orders.findIndex((o) => o.name === order.name);
                if (index !== -1) {
                    orders.splice(index, 1);
                    // @ts-ignore
                    this.$store.commit("setOrders", orders);
                    ElNotification({
                        title: "Success",
                        message: "Removed from order",
                        type: "success",
                    });
                    return;
                }
            },
        },
        data() {
            return {
                tables: [] as Table[],
                types: [] as { id: number, name: string }[],
                formRules: {
                    name: [
                        { required: true, message: 'Please enter a name.' }
                    ],
                    table: [
                        { required: true, message: 'Please select a table.' }
                    ],
                    type: [
                        { required: true, message: 'Please select a type.' }
                    ],
                    orders: [
                        { required: true, message: 'Please select an order.' }
                    ],
                }
            };
        },
        mounted() {
            this.fetchTables().then((tables) => {
                this.tables = tables
            })

            this.types = [
                { id: 0, name: "Order per table" },
                { id: 1, name: "Order per person" },
            ]
        },
        computed: {
            name: {
                get(): string {
                    // @ts-ignore
                    return this.$store.getters.getName;
                },
                set(value: string) {
                    // @ts-ignore
                    this.$store.commit("setName", value);
                },
            },

            table: {
                get(): number {
                    // @ts-ignore
                    return this.$store.getters.getTable;
                },
                set(value: number) {
                    // @ts-ignore
                    this.$store.commit("setTable", value);
                },
            },

            type: {
                get(): number {
                    // @ts-ignore
                    return this.$store.getters.getType;
                },
                set(value: number) {
                    // @ts-ignore
                    this.$store.commit("setType", value);
                },
            },

            orders: {
                get() {
                    // @ts-ignore
                    return this.$store.getters.getOrders;
                },
                set(value: number) {
                    // @ts-ignore
                    this.$store.commit("setOrders", value);
                },
            },
        }
    });
</script>
