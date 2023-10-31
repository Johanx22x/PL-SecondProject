<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50">
            <template #header>
                <el-text>
                    <h3>Healthy Menu Generator</h3>
                </el-text>
            </template>
            <el-form :model="form" ref="formRef" :rules="formRules" label-position="top">
                <el-form-item label="Maximum Calories" for="maxCalories" prop="maxCalories">
                    <el-input-number size="large" name="maxCalories" v-model.number="form.maxCalories" :min="0"/>
                </el-form-item>
                <el-form-item label="Drink" for="drink" prop="drink">
                    <el-checkbox v-model="form.wantDrink" name="drink" class="me-3" />
                    <el-select size="large" name="drink" v-model="form.drink" class="me-3" :disabled="!form.wantDrink">
                        <el-option
                            v-for="drink in drinks"
                            :key="drink.id"
                            :label="drink.name"
                            :value="drink.id"
                        />
                    </el-select>
                    <el-input-number size="large" name="drinkQuantity" placeholder="Amount" v-model.number="form.drinkQuantity" :min="0" :disabled="!form.wantDrink"/>
                </el-form-item>
                <el-form-item label="Protein" for="protein" prop="protein">
                    <el-checkbox v-model="form.wantProtein" name="protein" class="me-3" />
                    <el-select size="large" name="protein" v-model="form.protein" class="me-3" :disabled="!form.wantProtein">
                        <el-option
                            v-for="protein in proteins"
                            :key="protein.id"
                            :label="protein.name"
                            :value="protein.id"
                        />
                    </el-select>
                    <el-input-number size="large" name="proteinQuantity" placeholder="Amount" v-model.number="form.proteinQuantity" :min="0" :disabled="!form.wantProtein"/>
                </el-form-item>
                <el-form-item label="Side Dish" for="sideDish" prop="sideDish">
                    <el-checkbox v-model="form.wantSideDish" name="sideDish" class="me-3" />
                    <el-select size="large" name="sideDish" v-model="form.sideDish" class="me-3" :disabled="!form.wantSideDish">
                        <el-option
                            v-for="sideDish in sideDishes"
                            :key="sideDish.id"
                            :label="sideDish.name"
                            :value="sideDish.id"
                        />
                    </el-select>
                    <el-input-number size="large" name="sideDishQuantity" placeholder="Amount" v-model.number="form.sideDishQuantity" :min="0" :disabled="!form.wantSideDish"/>
                </el-form-item>
                <el-form-item label="Dessert" for="dessert" prop="dessert">
                    <el-checkbox v-model="form.wantDessert" name="dessert" class="me-3" />
                    <el-select size="large" name="dessert" v-model="form.dessert" class="me-3" :disabled="!form.wantDessert">
                        <el-option
                            v-for="dessert in desserts"
                            :key="dessert.id"
                            :label="dessert.name"
                            :value="dessert.id"
                        />
                    </el-select>
                    <el-input-number size="large" name="dessertQuantity" placeholder="Amount" v-model.number="form.dessertQuantity" :min="0" :max="3" :disabled="!form.wantDessert"/>
                </el-form-item>
            </el-form>
            <div class="d-flex flex-row justify-content-around">
                <el-button type="success" size="large" @click="submit()">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                    </template>
                    Generate
                </el-button>
                <el-button type="danger" class="text-decoration-none" size="large" tag="router-link" to='/orders/add' style="text-decoration: none;">
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
                // @ts-ignore
                let bodyFormData = new FormData();
                for (const [key, value] of Object.entries(this.form)) {
                    // @ts-ignore
                    bodyFormData.append(key, value);
                }
                let result = await axios.post("/api/food/", bodyFormData);
                if (result.status === 200) {
                    ElNotification({
                        type: 'success',
                        title: 'Success!',
                        message: 'Generated healthy dishes successfully!'
                    });
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
                    maxCalories: null,
                    wantDrink: null,
                    drink: null,
                    drinkQuantity: null,
                    wantProtein: null,
                    protein: null,
                    proteinQuantity: null,
                    wantSideDish: null,
                    sideDish: null,
                    sideDishQuantity: null,
                    wantDessert: null,
                    dessert: null,
                    dessertQuantity: null,
                },
                formRules: {
                    maxCalories: [
                        { required: true, message: 'Please input the maximum calories' },
                    ],
                }
            };
        },
    });
</script>
