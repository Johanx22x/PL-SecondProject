<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Edit {{ form.name }}</h3>
                </el-text>
            </template>
            <el-form :model="form" ref="formRef" label-position="top" :rules="formRules">
                <el-form-item label="Name" for="name" prop="name">
                    <el-input size="large" name="name" v-model="form.name" />
                </el-form-item>
                <el-form-item
                    v-for="(element, idx) in form.foods" :key="idx"
                    :prop="`foods.${idx}.id`"
                    :rules="{
                        required: true,
                        message: 'Food item can\'t be empty',
                        trigger: 'blur'
                    }"
                    class="w-100" >
                    <el-select 
                        size="large" 
                        v-model="element.id" 
                        class="w-100"
                        placeholder="Select an item" 
                        clearable
                        filterable >
                        <el-option
                            v-for="(option, idx) in allFoods" 
                            :key="idx" 
                            :value="option.id" :label="option.name" />
                    </el-select>
                    <el-button v-if="idx !== 0" type="danger" round class="mt-1" @click.prevent="removeItem(idx)">
                        <template #icon>
                            <font-awesome-icon icon="fa-solid fa-xmark" size="lg"/>
                        </template>
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button size="small" circle type="primary" @click.prevent="addItem()">
                        <template #icon>
                            <font-awesome-icon icon="fa-solid fa-plus" class="" size="lg" />
                        </template>
                    </el-button>
                </el-form-item>
            </el-form>
            <div class="d-flex flex-row justify-content-around">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Update 
                </el-button>
                <el-button type="danger" class="text-decoration-none" size="large" tag="router-link" to='/dishes'>
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
    import { ElNotification, FormInstance } from "element-plus";
    import Dish from "@/dish";
    import Food from "@/food";
    import axios from "axios";

    export default defineComponent({
        props: {
            id: {
                type: Number
            }
        },
        data() {
            return {
                form: {
                    name: "",
                    foods: [] as { id: number | null; }[]
                },
                formRules: {
                    name: [{
                        required: true, message: 'Please enter a name'
                    }],
                },
                allFoods: [] as Food[]
            }
        },
        methods: {
            addItem() {
                this.form.foods.push({ id: null });
            },
            removeItem(idx: number) {
                this.form.foods.splice(idx, 1);
            },
            async fetchDish(id: number) {
                return await axios.get<Dish>(`/api/dish/${id}`);
            },
            async fetchFoods() {
                return await axios.get<Food[]>('/api/food')
            },
            async submit() {
                (this.$refs["formRef"] as FormInstance).validate(async (valid, _) => {
                    if (valid) {
                        try {
                            await axios.post(`/api/dish/${this.id}`, this.form)
                            ElNotification({
                                type: 'success',
                                title: "Successfully updated dish",
                                message: "The dish has been successfully updated"
                            });
                            this.$router.push('/dishes');
                        } catch (e) {
                            ElNotification({
                                type: 'error',
                                title: "Couldn't update dish",
                                message: 'An error occurred while updating the dish'
                            });
                        }
                    }
                })
            },
        },
        async mounted() {
            try {
                // @ts-ignore: here id will always be a number, not undefined
                let res = await this.fetchDish(this.id);
                this.form.name = res.data.name
                this.form.foods = res.data.foods.map((food: Food) => { return  { id: food.id }});
            } catch (e) {
                ElNotification({
                    type: 'error',
                    title: "Couldn't load that dish",
                    message: 'An error occurred while loading the dish'
                });
                this.$router.push('/dishes');
            }
            try {
                let res = await this.fetchFoods();
                this.allFoods = res.data;
            } catch (e) {
                ElNotification({
                    type: 'error',
                    title: "Couldn't load foods"
                });
                this.$router.push('/dishes');
            }


        }
    });
</script>
