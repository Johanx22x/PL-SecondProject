<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Create New Food</h3>
                </el-text>
            </template>
            <el-form :model="form" ref="formRef" :rules="formRules" label-position="top">
                <el-form-item label="Name" for="name" prop="name">
                    <el-input size="large" name="name" v-model="form.name" />
                </el-form-item>
                <div class="d-flex flex-row justify-content-between">
                    <el-form-item label="Calories" for="calories" prop="calories">
                        <el-input-number size="large" name="calories" v-model.number="form.calories" :min="0"/>
                    </el-form-item>
                    <el-form-item 
                        label="Price"
                        for="price"
                        prop="price" >
                        <el-input-number size="large" name="price" v-model.number="form.price" :min="0"/>
                    </el-form-item>
                </div>
                <el-form-item label="Type" prop="subtype" for="type">
                    <el-cascader
                        size="large"
                        name="type"
                        :options="$store.state.foodTypes"
                        :props="{ expandTrigger: 'hover' }"
                        @change="(item) => {form.type = item[0]; form.subtype = item[1]}"
                        class="w-100" />
                </el-form-item>
            </el-form>
            <div class="d-flex flex-row justify-content-around">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Submit
                </el-button>
                <el-button type="danger" class="text-decoration-none" size="large" tag="router-link" to='/inventory'>
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
    import Food from "@/food";
    import type { FormInstance } from "element-plus";
    import { ElNotification } from "element-plus";
    import axios from "axios";

    export default defineComponent({
        methods: {
            submit() {
                (this.$refs["formRef"] as FormInstance).validate(async (valid: boolean, _) => {
                    if (valid) {
                        try {
                            await axios.post("/api/food/", this.form);
                            ElNotification({
                                type: 'success',
                                title: 'Success!',
                                message: 'Food created successfully!'
                            });
                            this.$router.push('/inventory');
                        } catch (e) {
                            ElNotification({
                                type: 'error',
                                title: 'Error creating food',
                                message: 'An error occurred while creating the food, please try again'
                            });
                        }
                    }
                });
            },
        },
        data() {
            return {
                form: {
                    name: "",
                    calories: 0.0,
                    price: 0.0,
                    type: 0,
                    subtype: 0
                } as Food,
                formRules: {
                    name: [
                        { required: true, message: 'Please enter a name.' }
                    ],
                    price: { 
                        required: true,
                        type: 'number',
                        asyncValidator: (_: any, value: number) => {
                            return new Promise((resolve, reject) => {
                                if (value < 1) {
                                    reject('Price must be greater than 0')
                                } else {
                                    resolve(null);
                                }
                            });
                        }
                    },
                    subtype: {
                        required: true,
                        type: 'number',
                        asyncValidator: (_: any, value: number) => {
                            return new Promise((resolve, reject) => {
                                if (value === 0) {
                                    reject('Please select a type and subtype');
                                } else {
                                    resolve(null);
                                }
                            });
                        }
                    }
                }
            };
        },
    });
</script>
