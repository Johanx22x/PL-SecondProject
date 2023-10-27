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
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    },
    {
        path: '/inventory',
        name: 'Inventory',
        component: () => import(/* webpackChunkName: "inventory" */"../views/InventoryView.vue")
    },
    {
        path: '/statistics',
        name: 'Statistics',
        component: () => import(/* webpackChunkName: "inventory" */"../views/StatisticsView.vue")
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import(/* webpackChunkName: "not-found" */ '../views/NotFoundView.vue')
    }
]

const router = createRouter({
    // history: createWebHistory(),
    history: createWebHashHistory(),
    routes
})

export default router
