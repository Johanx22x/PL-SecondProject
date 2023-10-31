<template>
    <el-container class="container-sm d-flex flex-column">
        <el-header class="m-0 p-0 mt-5 text-start h-100 w-100">
            <el-text><h1>Configuration</h1></el-text>
            <el-divider></el-divider>
        </el-header>
        <el-main>
            <el-container class="container-sm d-flex flex-row justify-content-between">
                <el-text><h3>Avaliable Tables</h3></el-text>
                <el-button type="primary" class="m-2" size="large" @click="$router.push('/configuration/table/add')">
                    <template #icon>
                        <font-awesome-icon icon="fa-solid fa-plus" size="xl" />
                    </template>
                    Add Table 
                </el-button>
            </el-container>
            <el-table :data="tables" stripe>
                <el-table-column prop="name" label="Name"></el-table-column>
                <el-table-column prop="people" label="Max People"></el-table-column>
                <!-- action (DELETE) -->
                <el-table-column label="Actions">
                    <template #default="scope">
                        <el-button type="danger" class="text-decoration-none m-0" size="large" @click="deleteTable(scope.row.id)">
                            <template #icon>
                                <font-awesome-icon icon="fa-solid fa-trash" size="xl" />
                            </template>
                            Delete 
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-main>
    </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import Table from '@/table'

export default defineComponent({
    name: 'ConfigurationView',
    data() {
        return {
            tables: [] as Table[],
        }
    },
    methods: {
        async fetchTables() {
            let res = await axios.get('/api/table')
            return res.data
        },
        async deleteTable(id: number) {
            await axios.delete(`/api/table/${id}`)
            this.tables = this.tables.filter((table) => table.id != id)
        },
    },
    mounted() {
        this.fetchTables().then((data) => {
            this.tables = data
        })
    },
})
</script>
