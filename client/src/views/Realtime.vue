<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <h3>Realtime Demo</h3>
        <hr>
        <p>
          This map will update in realtime as GPS Messages are added to the DB.
          The record is pushed to Redis from inside Django, and then it is sent to
          the browser via websocket. This happens in the <code>realtime_ws_server.py</code> script.
        </p>

        <p>
          Flick the switch below to POST a new GPS Message to the server every second (like a PUC would).
          The data that shows in the box is NOT from the POST response, it's comes in realtime
          from the websocket and get's inserted into the Vuex store.
        </p>

        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>Data</span>
            <el-switch v-model="post_mock_data"
                       inactive-color="#b9bcc3"
                       :width="50"
                       style="float: right;"></el-switch>
          </div>
          <div class="text" style="overflow-x: auto">
            <pre><code>{{ formatted_data }}</code></pre>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <GmapMap
          :center="center_coords"
          :zoom="17"
          ref="mapRef"
          map-type-id="satellite"
          style="width: 100%; height: 500px;"
        >
            <GmapMarker v-if="ready_for_marker" :position="marker_coords"/>
        </GmapMap>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Vue from 'vue'
import moment from 'moment'
import config from 'config'
import async from 'neo-async'
import { postGpsMessage } from '@/api/data'
import { generateRandomPoint } from '@/utils/random-geo'
import { load, loaded, gmapApi, Marker } from 'vue2-google-maps'

export default {
  mounted () {
    // Switch out the markers once google maps has finished loading
    loaded.then(() => {
      import('marker-animate-unobtrusive').then(SlidingMarker => {
        SlidingMarker.initializeGlobally()
        this.ready_for_marker = true
      })

    })
  },
  beforeDestroy () {
    this.post_mock_data = false
  },
  data() {
    return {
      post_mock_data: false,
      ready_for_marker: false,
      center_coords: { // These are from around Springfield, MO
        lat: 37.2911873,
        lng: -93.5630069
      }
    }
  },
  computed: {
    google: gmapApi,
    marker_coords() {
      let data = this.$store.state.socket.data
      if (data.hasOwnProperty('latitude')) {
        return {
          lat: Number(data.latitude),
          lng: Number(data.longitude)
        }
      } else {
        return this.center_coords
      }
    },
    formatted_data() {
      return JSON.stringify(this.$store.state.socket.data, null, 4)
    }
  },
  watch: {
    post_mock_data () {
      // If the switch is active, post a new gps message every second.
      async.doWhilst(
          (cb) => {
              setTimeout(() => {
                this.postMockGpsMessage()
                  cb();
              }, 1000);
          },
          () => (this.post_mock_data === true)
      )
    }
  },
  methods: {
    postMockGpsMessage () {
      /*
       * Generates random data and posts a new GPS Messages.
       * I change the coords just a little bit, so the marker moves around on the map
       */
      let randomCoords = generateRandomPoint(this.marker_coords, 15)
      const data = {
        "puc": `${config.api.baseUrl}pucs//8765`,
        "latitude": (randomCoords.lat).toFixed(14),
        "longitude": (randomCoords.lng).toFixed(14),
        "groundspeed": 0.01841250000000,
        "truecourse": 5.10000610000000,
        "timestamp": moment().format("YYYY-MM-DD HH:mm:ss")
      }

      // Do nothing with the post response. Our data will come in through the websocket.
      postGpsMessage(data)
    }
  }
}
</script>
