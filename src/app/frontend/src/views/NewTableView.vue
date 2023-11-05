<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Create New Table</h3>
                </el-text>
            </template>
            <el-form :model="form" ref="formRef" :rules="formRules" label-position="top">
                <el-form-item label="Name" for="name" prop="name">
                    <el-input size="large" name="name" v-model="form.name" />
                </el-form-item>
                <el-form-item label="Max People" for="people" prop="people">
                    <el-input-number size="large" name="people" v-model="form.people" min="1" />
                </el-form-item>
            </el-form>
            <div class="d-flex flex-row justify-content-around">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Submit
                </el-button>
                <el-button type="danger" class="text-decoration-none" size="large" tag="router-link" to='/configuration'>
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
    import Table from "@/table";
    import type { FormInstance } from "element-plus";
    import { ElNotification } from "element-plus";
    import axios from "axios";

    export default defineComponent({
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
            async formWasValid() {
                let result = await axios.post("/api/table/", this.form);
                if (result.status === 200) {
                    ElNotification({
                        type: 'success',
                        title: 'Success!',
                        message: 'Table was added successfully!'
                    });
                    this.$router.push('/configuration');
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
                form: {
                    name: '',
                    people: 0,
                } as Table,
                formRules: {
                    name: [
                        { required: true, message: 'Please enter a name.' }
                    ],
                    people: [
                        { required: true, message: 'Please enter a number of people.' }
                    ]
                }
            };
        },
    });
</script>
