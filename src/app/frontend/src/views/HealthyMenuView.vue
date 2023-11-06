<template>
    <el-container class="container-sm justify-content-around">
        <el-card class="mt-5 w-50 h-50 mb-5">
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
                    <el-select size="large" name="drink" v-model="form.drink" class="me-3" :disabled="!form.wantDrink" multiple>
                        <el-option
                            v-for="drink in drinks"
                            :key="drink.value"
                            :label="drink.label"
                            :value="drink.value"
                        />
                    </el-select>
                    <el-input-number size="large" name="drinkQuantity" placeholder="Amount" v-model.number="form.drinkQuantity" :min="0" :disabled="!form.wantDrink"/>
                </el-form-item>
                <el-form-item label="Protein" for="protein" prop="protein">
                    <el-checkbox v-model="form.wantProtein" name="protein" class="me-3" />
                    <el-select size="large" name="protein" v-model="form.protein" class="me-3" :disabled="!form.wantProtein" multiple>
                        <el-option
                            v-for="protein in proteins"
                            :key="protein.value"
                            :label="protein.label"
                            :value="protein.value"
                        />
                    </el-select>
                    <el-input-number size="large" name="proteinQuantity" placeholder="Amount" v-model.number="form.proteinQuantity" :min="0" :disabled="!form.wantProtein"/>
                </el-form-item>
                <el-form-item label="Side Dish" for="sideDish" prop="sideDish">
                    <el-checkbox v-model="form.wantSideDish" name="sideDish" class="me-3" />
                    <el-select size="large" name="sideDish" v-model="form.sideDish" class="me-3" :disabled="!form.wantSideDish" multiple>
                        <el-option
                            v-for="sideDish in sideDishes"
                            :key="sideDish.value"
                            :label="sideDish.label"
                            :value="sideDish.value"
                        />
                    </el-select>
                    <el-input-number size="large" name="sideDishQuantity" placeholder="Amount" v-model.number="form.sideDishQuantity" :min="0" :disabled="!form.wantSideDish"/>
                </el-form-item>
                <el-form-item label="Dessert" for="dessert" prop="dessert">
                    <el-checkbox v-model="form.wantDessert" name="dessert" class="me-3" />
                    <el-select size="large" name="dessert" v-model="form.dessert" class="me-3" :disabled="!form.wantDessert" multiple>
                        <el-option
                            v-for="dessert in desserts"
                            :key="dessert.value"
                            :label="dessert.label"
                            :value="dessert.value"
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
                <el-button type="primary" class="text-decoration-none" size="large" tag="router-link" to='/orders/menu' style="text-decoration: none;">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-arrow-left" size="xl" />
                    </template>
                    Go Back
                </el-button>
            </div>
            <el-divider />
            <el-scrollbar style="height: 300px;">
                <el-card v-for="menu in generated" :key="menu.id" class="me-5 ms-5 mb-3">
                    <h5>{{ menu.args[0].join(", ") }}</h5>
                    <h5>Price: </h5> ${{ menu.args[1] }}
                    <el-divider />
                    <el-button type="success" size="large" @click="addToOrder(menu)">
                        <template #icon>
                            <font-awesome-icon icon="fa-solid fa-check" size="xl" />
                        </template>
                        Add to Order 
                    </el-button>
                </el-card>
            </el-scrollbar>
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
            async addToOrder(menu: any) {
                let foods = await axios.get("/api/food/");

                let form = {
                    name: "Auto-Generated Healthy Dish",
                    foods: foods.data.filter((food: any) => {
                        return menu.args[0].includes(food.name);
                    }),
                    is_predef: 0,
                }

                if (form.foods.length === 0) {
                    ElNotification({
                        type: 'error',
                        title: 'Error!',
                        message: 'Something went wrong!'
                    });
                    return;
                }

                try {
                    let res = await axios.post("/api/dish/", form);
                    let order = res.data;

                    // @ts-ignore
                    let orders = this.$store.getters.getOrders;

                    orders.push({
                        id: order.id,
                        name: order.name,
                        price: order.foods.reduce((acc: number, food: any) => {
                            return acc + food.price;
                        }, 0).toFixed(2),
                        quantity: 1,
                    });

                    // @ts-ignore
                    this.$store.commit("setOrders", orders);

                    ElNotification({
                        type: 'success',
                        title: 'Success!',
                        message: 'Added to order successfully!'
                    });
                } catch (e) {
                    ElNotification({
                        type: 'error',
                        title: 'Error!',
                        message: 'Something went wrong!'
                    });
                }
            },
            submit() {
                (this.$refs["formRef"] as FormInstance).validate(async (valid: boolean, _) => {
                    if (!valid) {
                        this.formWasInvalid();
                        return;
                    }

                    let query = "get_menu(";

                    if (this.form.wantDrink) {
                        query += `1, [${this.form.drink}], ${this.form.drinkQuantity}, `;
                    } else {
                        query += "1, [], 0, ";
                    }

                    if (this.form.wantProtein) {
                        query += `2, [${this.form.protein}], ${this.form.proteinQuantity}, `;
                    } else {
                        query += "2, [], 0, ";
                    }

                    if (this.form.wantSideDish) {
                        query += `3, [${this.form.sideDish}], ${this.form.sideDishQuantity}, `;
                    } else {
                        query += "3, [], 0, ";
                    }

                    if (this.form.wantDessert) {
                        query += `4, [${this.form.dessert}], ${this.form.dessertQuantity}, `;
                    } else {
                        query += "4, [], 0, ";
                    }

                    query += `${this.form.maxCalories}, Menu).`;

                    // Clean query from whitespaces
                    query = query.replace(/\s/g, "");

                    try { 
                        let res = await this.query(query);

                        // @ts-ignore
                        this.generated = res.data[0].Menu;

                        ElNotification({
                            type: 'success',
                            title: 'Success!',
                            message: 'Generated menu successfully!'
                        });
                    } catch (e) {
                        ElNotification({
                            type: 'error',
                            title: 'Error!',
                            message: 'Something went wrong!'
                        });
                    }
                });
            },
            formWasInvalid() {
                ElNotification({
                    type: 'error',
                    title: 'Error!',
                    message: 'One or more fields are invalid!'
                });
            },
            async query(query: string) {
                let res = await axios.post(`/api/prolog/${query}`);
                return res;
            },
        },
        data() {
            return {
                drinks: [],
                proteins: [],
                sideDishes: [],
                desserts: [],
                form: {
                    maxCalories: null,
                    wantDrink: null,
                    drink: [],
                    drinkQuantity: 0,
                    wantProtein: null,
                    protein: [],
                    proteinQuantity: 0,
                    wantSideDish: null,
                    sideDish: [],
                    sideDishQuantity: 0,
                    wantDessert: null,
                    dessert: [],
                    dessertQuantity: 0,
                },
                formRules: {
                    maxCalories: [
                        { required: true, message: 'Please input the maximum calories' },
                    ],
                },
                generated: [],
            };
        },
        mounted() {
            // @ts-ignore
            this.drinks = this.$store.getters.getDrinks;
            // @ts-ignore
            this.proteins = this.$store.getters.getProteins;
            // @ts-ignore
            this.sideDishes = this.$store.getters.getSideDishes;
            // @ts-ignore
            this.desserts = this.$store.getters.getDesserts;
        },
    });
</script>
