<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navItems = [
  { name: '首页', path: '/' },
  { name: '图像语义分割', path: '/image-detection' },
  { name: '实时语义分割', path: '/realtime-detection' }
]

const handleLogout = () => {
  localStorage.removeItem('loggedIn')
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-logo">
        <span class="logo-icon"></span>
        <span class="logo-text">语义分割平台</span>
      </router-link>
      <div class="navbar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
        >
          {{ item.name }}
        </router-link>
      </div>
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
  height: 60px;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #1e293b;
}

.logo-icon {
  font-size: 1.5rem;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: 600;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar-nav {
  display: flex;
  gap: 2px;
}

.nav-item {
  padding: 10px 20px;
  text-decoration: none;
  color: #64748b;
  font-size: 0.95rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: #1e293b;
  background: rgba(99, 102, 241, 0.1);
}

.nav-item.active {
  color: #fff;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.logout-btn {
  padding: 8px 20px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.15);
}
</style>
