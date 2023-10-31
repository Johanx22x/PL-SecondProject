import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        component: HomeView
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/AboutView.vue')
    },
    {
        path: '/inventory',
        name: 'Inventory',
        component: () => import(/* webpackChunkName: "inventory" */"@/views/InventoryView.vue")
    },
    {
        path: '/inventory/add',
        name: 'Add Food',
        component: () => import(/* webpackChunkName: "new_food" */"@/views/NewFoodView.vue")
    },
    {
        path: '/inventory/edit/:id',
        name: 'Edit Food',
        component: () => import(/* webpackChunkName: "edit_food" */"@/views/EditFoodView.vue")
    },
    {
        path: '/invoices',
        name: 'Invoices',
        component: () => import(/* webpackChunkName: "invoices" */"@/views/InvoicesView.vue")
    },
    {
        path: '/statistics',
        name: 'Statistics',
        component: () => import(/* webpackChunkName: "statistics" */"@/views/StatisticsView.vue")
    },
    {
        path: '/dishes',
        name: 'Dishes',
        component: () => import(/* webpackChunkName: "dishes"*/ "@/views/DishesView.vue")
    },
    {
        path: '/dishes/add',
        name: 'Add Dish',
        component: () => import(/* webpackChunkName: "new_dish"*/ "@/views/NewDishView.vue")
    },
    {
        path: '/dishes/edit/:id',
        name: 'Edit Dish',
        component: () => import(/* webpackChunkName: "new_dish"*/ "@/views/EditDishView.vue"),
        props: true
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import(/* webpackChunkName: "not-found" */ '@/views/NotFoundView.vue')
    },
]

const router = createRouter({
    // history: createWebHistory(),
    history: createWebHashHistory(),
    routes
})

export default router
