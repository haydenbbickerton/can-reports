<style lang="scss" scoped>

</style>

<template>
  <div class="app-container">

    <el-card class="box-card" v-loading="loading">
      <div slot="header" class="clearfix">
        <span>PUC Messages Summary Statistics</span>
        <el-button type="primary" @click="fetchReport" style="float: right;">Refresh</el-button>
      </div>

      <el-table
        :data="formatted_data"
        :show-header="false"
        stripe
        class="summary-report">
          <el-table-column
            prop="title">
          </el-table-column>
          <el-table-column
            prop="value">
          </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import moment from 'moment'
import humanizeDuration from 'humanize-duration'
import { getPucMessagesReport } from '@/api/data'

export default {
  data() {
    return {
      loading: false,
      summary_data: {
        // Not storing this data in vuex store, as it won't be used anywhere else
      }
    }
  },
  computed: {
    formatted_data() {
      /*
       * The data as it come from the API is not pretty. Format it first.
       */
      const data = this.summary_data

      if (Object.keys(data).length > 0) {

        let newd = [];

        newd.push(['Total CAN Messages', data['total_can']])
        newd.push(['Total GPS Messages', data['total_gps']])
        newd.push(['Total Runtime', humanizeDuration(data['total_runtime'] * 1000)])
        newd.push(['Total Unique CAN Messages', data['unique_can_count']])
        newd.push(['Average CAN Messages Per Second', (data['avg_can_per_sec']).toFixed(2)])
        newd.push(['Average GPS Messages Per Second', (data['avg_gps_per_sec']).toFixed(2)])
        newd.push(['Timestamp Containing The Most CAN Messages', moment(data['timestamp_with_most_cans']).format("YYYY-MM-DD HH:mm:ss")])
        newd.push(['Timestamp Containing The Least CAN Messages', moment(data['timestamp_with_least_cans']).format("YYYY-MM-DD HH:mm:ss")])

        return newd.map(row => ({title: row[0],  value: row[1]}))
      }
    }
  },
  methods: {
    fetchReport() {
      this.loading = true
      getPucMessagesReport().then(response => {
        this.summary_data = Object.assign({}, this.summary_data, response.data)  // Have to do Object.assign to keep it reactive
        this.loading = false
      })
    }
  }
}
</script>



