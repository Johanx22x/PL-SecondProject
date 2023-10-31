<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Create New Order</h3>
                </el-text>
            </template>
            <el-form :model="form" ref="formRef" :rules="formRules" label-position="top">
                <el-form-item label="Name" for="name" prop="name">
                    <el-input size="large" name="name" v-model="form.name" />
                </el-form-item>
                <div class="d-flex flex-row justify-content-between">
                    <el-form-item label="Table" for="table" prop="table">
                        <el-select size="large" name="table" v-model="form.table">
                            <el-option
                                v-for="table in tables"
                                :key="table.id"
                                :label="table.name"
                                :value="table.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Type" for="type" prop="type">
                        <el-select size="large" name="type" v-model="form.type">
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
                    <el-table :data="form.orders" style="width: 100%">
                        <el-table-column prop="name" label="Name" />
                        <el-table-column prop="price" label="Price" />
                        <el-table-column prop="quantity" label="Quantity" />
                    </el-table>
                    <el-button type="primary" size="large" @click="addOrder()" class="mt-3">
                        <template #icon>
                            <font-awesome-icon icon="fa-solid fa-plus" size="xl" />
                        </template>
                        Add Order 
                    </el-button>
                </el-form-item>
                <el-text><h5>Total: $</h5></el-text>
            </el-form>
            <div class="d-flex flex-row justify-content-around">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Submit
                </el-button>
                <el-button type="danger" class="text-decoration-none" size="large" tag="router-link" to='/orders' style="text-decoration: none;">
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
                    } else {
                        this.formWasInvalid();
                    }
                });
            },
            goBack() {
            },
            async formWasValid() {
                // @ts-ignore
                let bodyFormData = new FormData();
                for (const [key, value] of Object.entries(this.form)) {
                    // @ts-ignore
                    bodyFormData.append(key, value);
                }
                let result = await axios.post("/api/order", bodyFormData);
                if (result.status === 200) {
                    ElNotification({
                        type: 'success',
                        title: 'Success!',
                        message: 'Food created successfully!'
                    });
                    this.$router.push('/inventory');
                }
            },
            formWasInvalid() {
                ElNotification({
                    type: 'error',
                    title: 'Error!',
                    message: 'One or more fields are invalid!'
                });
            }

        },
        data() {
            return {
                tables: [] as Table[],
                types: [] as { id: number, name: string }[],
                form: {
                    name: "",
                    table: null,
                    type: null,
                    orders: null,
                },
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
        }
    });
</script>
