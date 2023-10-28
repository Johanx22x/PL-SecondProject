<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Edit Food: {{ form.name }}</h3>
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
                    <el-form-item label="Price" for="price" prop="price">
                        <el-input-number size="large" name="price" v-model.number="form.price" :min="0"/>
                    </el-form-item>
                </div>
                <el-form-item label="Type" prop="type" for="type">
                    <el-cascader
                        size="large"
                        name="type"
                        v-model="this.default"
                        :options="$store.state.foodTypes"
                        :props="{ expandTrigger: 'hover' }"
                        @change="(item) => {form.type = item[0]; form.subtype = item[1]; this.default = [item[0], item[1]]}"
                        class="w-100" />
                </el-form-item>
            </el-form>
            <div class="d-flex flex-row justify-content-around">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Update
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
        async mounted() {
            let result = await axios.get("/api/food/" + this.$route.params.id);
            if (result.status === 200) {
                this.form = result.data;
            }

            this.default = [this.form.type, this.form.subtype];
        },
        methods: {
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
                let result = await axios.post("/api/food/" + this.$route.params.id + "/update", bodyFormData);
                if (result.status === 200) {
                    ElNotification({
                        type: 'success',
                        title: 'Success!',
                        message: 'Food updated successfully!'
                    });
                    this.$router.push("/inventory");
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
                default: [0, 0],
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
                    calories: [
                        { required: true, message: 'Please enter some calories.' },
                    ],
                    price: [
                        { required: true, message: 'Please enter a price.' },
                    ],
                    type: [
                        {
                            required: true,
                            message: 'Please select the food\'s type',
                            trigger: 'change'
                        }
                    ]
                }
            };
        },
    });
</script>
