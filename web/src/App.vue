<script setup lang="ts">
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

const route = useRoute()

const showNavAndFooter = route.path !== '/login'
</script>

<template>
  <div class="app">
    <Navbar v-if="showNavAndFooter" />
    <main>
      <router-view />
    </main>
    <Footer v-if="showNavAndFooter" />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
