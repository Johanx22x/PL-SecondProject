<template>
  <el-container class="container-xl mt-5 h-100 w-100">
    <el-header class="m-0 p-0 text-start h-100 w-100">
      <el-text><h1>Statistics</h1></el-text>
      <el-divider></el-divider>
    </el-header>
    <el-container>
      <el-aside>

        <el-card class="box-card m-3" shadow="hover">
          <el-statistic :value="totalSales" :precision="2">
            <template #prefix>
                <font-awesome-icon class="me-1" icon="fa-solid fa-dollar-sign"/>
            </template>
            <template #title>
                <el-container style="display: inline-flex">
                    <h5>Total sales</h5>
                    <el-tooltip
                    effect="dark"
                    content="Total sales since the restaurant opened"
                    placement="top"
                  >
                    <el-icon style="margin-left: 4px" :size="16">
                      <Warning />
                    </el-icon>
                  </el-tooltip>
                </el-container>
            </template>
          </el-statistic>
        </el-card>

        <el-card class="box-card m-3" shadow="hover">
          <el-statistic :value="inventoryItems">
            <template #prefix>
                <font-awesome-icon class="me-1" icon="fa-solid fa-drumstick-bite" />
            </template>
            <template #title>
                <el-container style="display: inline-flex">
                    <h5>Inventory items</h5>
                    <el-tooltip
                    effect="dark"
                    content="Number of individual foods in inventory"
                    placement="top"
                  >
                    <el-icon style="margin-left: 4px" :size="16">
                      <Warning />
                    </el-icon>
                  </el-tooltip>
                </el-container>
            </template>
          </el-statistic>
        </el-card>

        <el-card class="box-card m-3" shadow="hover">
          <el-statistic :value="menuItems">
            <template #prefix>
                <font-awesome-icon class="me-1" icon="fa-solid fa-utensils" />
            </template>
            <template #title>
                <el-container style="display: inline-flex">
                    <h5>Menu items</h5>
                    <el-tooltip
                    effect="dark"
                    content="Number of dishes available to order"
                    placement="top"
                  >
                    <el-icon style="margin-left: 4px" :size="16">
                      <Warning />
                    </el-icon>
                  </el-tooltip>
                </el-container>
            </template>
          </el-statistic>
        </el-card>

        <el-card class="box-card m-3" shadow="hover">
          <el-statistic :value="totalOrders">
            <template #prefix>
                <font-awesome-icon class="me-1" icon="fa-solid fa-receipt" />
            </template>
            <template #title>
                <el-container style="display: inline-flex">
                    <h5>Total orders</h5>
                    <el-tooltip
                    effect="dark"
                    content="Number of orders placed since the restaurant opened"
                    placement="top"
                  >
                    <el-icon style="margin-left: 4px" :size="16">
                      <Warning />
                    </el-icon>
                  </el-tooltip>
                </el-container>
            </template>
          </el-statistic>
        </el-card>

      </el-aside> 

      <el-main class="p-0 m-0 h-100 w-100">

          <el-card class="m-3 text-start" shadow="hover">
              <el-container>
                  <el-text><h4>Sales by date range</h4></el-text>
                  <el-date-picker
                      v-model="value"
                      type="daterange"
                      unlink-panels
                      range-separator="To"
                      start-placeholder="Start date"
                      end-placeholder="End date"
                      :shortcuts="shortcuts"
                      class="ms-5"
                      @change="async () => {
                          this.salesData = await this.fetchSalesByDateRange(this.value[0], this.value[1])
                          salesData.forEach((row) => {
                              row[0] = new Date(row[0])
                              row[0] = new Date(row[0].getTime() + Math.abs(row[0].getTimezoneOffset()*60000))
                          })
                          if (this.salesData.length == 0) {
                              this.salesData = [[new Date(), 0, 0]]
                          }
                          this.drawSalesIncomeChart()
                      }"
                      />
              </el-container>
              <el-divider/>
              <el-container class="d-flex flex-column align-items-center">
                  <div id="sales-income-chart" class="w-100" style="height: 500px"></div>
              </el-container>
          </el-card>

          <el-card class="m-3 text-start" shadow="hover">
              <el-text><h4>Trending Dishes</h4></el-text>
              <el-divider/>
              <el-container class="d-flex flex-column align-items-center">
                  <div id="dishes-chart" class="w-100" style="height: 300px"></div>
              </el-container>
          </el-card>

          <el-card class="m-3 text-start" shadow="hover">
              <el-text><h4>Trending Healthy Foods</h4></el-text>
              <el-divider/>
              <el-container class="d-flex flex-column align-items-center">
                  <div id="inventory-chart" class="w-100" style="height: 300px"></div>
              </el-container>
          </el-card>

      </el-main>

    </el-container>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import Statistic from '@/statistic'
import {
  Warning,
} from '@element-plus/icons-vue'

const shortcuts = [
  {
    text: 'Last week',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    },
  },
  {
    text: 'Last month',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    },
  },
  {
    text: 'Last 3 months',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    },
  },
  {
    text: 'Last year',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
      return [start, end]
    },
  },
]

// @ts-ignore
google.charts.load('current', {'packages':['bar', 'line']});

export default defineComponent({
  name: 'StatisticsView',
  components: {
    Warning,
  },
  methods: {
    async fetchStatistics() {
      let res = await axios.get<Statistic>('/api/statistic/latest')
      return res
    },

    async fetchSalesByDateRange(startDate: Date, endDate: Date) {
      let res = await axios.get<Array<Array<any>>>('/api/statistic/date-range', {
        params: {
          start: startDate,
          end: endDate
        }
      })
      return res.data
    },

    async fetchTopInventoryItems() {
      let res = await axios.get<Array<Array<any>>>('/api/statistic/top-inventory-items')
      return res.data
    },

    async fetchTopMenuItems() {
      let res = await axios.get<Array<Array<any>>>('/api/statistic/top-menu-items')
      return res.data
    },

    drawSalesIncomeChart() {
        // @ts-ignore
          var data = new google.visualization.DataTable();
          data.addColumn('date', 'Date');
          data.addColumn('number', 'Sales');
          data.addColumn('number', 'Income');

          data.addRows(this.salesData);

          var options = {
            chart: {
              title: 'Sales and Income',
              subtitle: 'Sales and Income by Date',
            },
            hAxis: {
              title: 'Date',
              format: 'd/M/yy',
            },
            series: {
              0: {axis: 'Sales'}, 
              1: {axis: 'Income (USD)'},
            },
            axes: {
              y: {
                Sales: {label: 'Sales'}, 
                'Income (USD)': {label: 'Income (USD)'},
              },
            },
          };

        // @ts-ignore
          var chart = new google.charts.Line(document.getElementById('sales-income-chart'));

        // @ts-ignore
          chart.draw(data, google.charts.Line.convertOptions(options));
    },

    drawInventoryChart() {
        // @ts-ignore
        var data = google.visualization.arrayToDataTable(this.inventoryData);

        var options = {
          chart: {
            title: 'Top 3 inventory items',
            subtitle: 'Sales by inventory item',
          },
          bars: 'horizontal', // Required for Material Bar Charts.
          vAxis: {
            title: 'Inventory item',
          },
          hAxis: {
            title: 'Sales',
            minValue: 0,
          },
        };

        // @ts-ignore
        var chart = new google.charts.Bar(document.getElementById('inventory-chart'));

        // @ts-ignore
        chart.draw(data, google.charts.Bar.convertOptions(options));
    },

    drawDishesChart() {
        // @ts-ignore
        var data = google.visualization.arrayToDataTable(this.menuData);

        var options = {
          chart: {
            title: 'Top 3 menu dishes',
            subtitle: 'Sales by dish',
          },
          bars: 'horizontal', // Required for Material Bar Charts.
          vAxis: {
            title: 'Dish',
          },
          hAxis: {
            title: 'Sales',
            minValue: 0,
          },
        };

        // @ts-ignore
        var chart = new google.charts.Bar(document.getElementById('dishes-chart'));

        // @ts-ignore
        chart.draw(data, google.charts.Bar.convertOptions(options));
    },
  },
  async mounted() {
    let latestStatistic = await this.fetchStatistics()

    this.totalSales = latestStatistic.data.total_sales
    this.inventoryItems = latestStatistic.data.inventory_items
    this.menuItems = latestStatistic.data.menu_items
    this.totalOrders = latestStatistic.data.total_orders

    let res = await this.fetchSalesByDateRange(this.value[0], this.value[1])
    if (res.length !== 0) {
        this.salesData = res
    }

    this.inventoryData.push(...await this.fetchTopInventoryItems())
    this.menuData.push(...await this.fetchTopMenuItems())

    // Load google charts 
    // @ts-ignore
    google.charts.setOnLoadCallback(this.drawInventoryChart);
    // @ts-ignore
    google.charts.setOnLoadCallback(this.drawDishesChart);
    // @ts-ignore
    google.charts.setOnLoadCallback(this.drawSalesIncomeChart);
  },
  data() {
    return {
      shortcuts,
      inventoryData: [["Name", "Sales"]],
      menuData: [["Name", "Sales"]],
      salesData: [[new Date(), 0, 0]],
      totalSales: 0.0,
      inventoryItems: 0,
      menuItems: 0,
      totalOrders: 0,
      value: [new Date(), new Date()],
    }
  },
})
</script>
