import { createStore } from 'vuex'

export default createStore({
    state: {
        order: {
            name: "",
            table: null,
            type: null,
            orders: [],
        },
        foodTypes: [
            {
                label: "Drink",
                value: 1,
                children: [
                    {
                        label: "Soda",
                        value: 1
                    },
                    {
                        label: "Natural",
                        value: 2
                    },
                    {
                        label: "Water Based",
                        value: 3
                    },
                    {
                        label: "Milk Based",
                        value: 4
                    },
                    {
                        label: "Hot",
                        value: 5
                    },
                    {
                        label: "Cold",
                        value: 6
                    }
                ]
            },
            {
                label: "Protein",
                value: 2,
                children: [
                    {
                        label: "Red Meat",
                        value: 7
                    },
                    {
                        label: "Chicken",
                        value: 8
                    },
                    {
                        label: "Fish",
                        value: 9
                    },
                    {
                        label: "Seafood",
                        value: 10
                    }
                ]
            },
            {
                label: "Side Dish",
                value: 3,
                children: [
                    {
                        label: "Vegetables",
                        value: 11
                    },
                    {
                        label: "Carbs",
                        value: 12
                    },
                    {
                        label: "Hot",
                        value: 5
                    },
                    {
                        label: "Cold",
                        value: 6
                    }
                ]
            },
            {
                label: "Dessert",
                value: 4,
                children: [
                    {
                        label: "Lactose",
                        value: 13
                    },
                    {
                        label: "No Lactose",
                        value: 14,
                    },
                    {
                        label: "Fruit",
                        value: 15
                    }
                ]
            }
        ],
        paymentTypes: [
            {
                label: "Cash",
                value: 1
            },
            {
                label: "Credit Card",
                value: 2
            }
        ],
    },
    getters: {
        getOrder(state) {
            return state.order;
        },
        getName(state) {
            return state.order.name;
        },
        getTable(state) {
            return state.order.table;
        },
        getType(state) {
            return state.order.type;
        },
        getOrders(state) {
            return state.order.orders;
        },
        getDrinks(state) {
            return state.foodTypes[0].children;
        },
        getProteins(state) {
            return state.foodTypes[1].children;
        },
        getSideDishes(state) {
            return state.foodTypes[2].children;
        },
        getDesserts(state) {
            return state.foodTypes[3].children;
        }
    },
    mutations: {
        setName(state, name) {
            state.order.name = name;
        },
        setTable(state, table) {
            state.order.table = table;
        },
        setType(state, type) {
            state.order.type = type;
        },
        setOrders(state, orders) {
            state.order.orders = orders;
        },
        clearOrder(state) {
            state.order = {
                name: "",
                table: null,
                type: null,
                orders: [],
            }
        },
    },
    actions: {
    },
    modules: {
    }
})
