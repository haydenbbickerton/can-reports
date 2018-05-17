<template>
  <div id="app">
  	<transition name="fade" mode="out-in">
    	<router-view></router-view>
    </transition>
  </div>
</template>

<script>
import request from '@/utils/request'

export default {
  name: 'app',
  mounted () {
  	// Do a blank request to trigger login if they aren't
    request.get('/')

    // Start listening
    this.$store.dispatch('socket/listenToSocket')
  }
}
</script>
