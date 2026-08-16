<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMsg = ref('')

const handleLogin = () => {
  if (username.value === 'admin' && password.value === '123456') {
    localStorage.setItem('loggedIn', 'true')
    router.push('/')
  } else {
    errorMsg.value = '用户名或密码错误'
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>语义分割平台</h1>
          <p>请登录系统</p>
        </div>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="请输入用户名"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="请输入密码"
              class="form-input"
            />
          </div>
          <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
          <button type="submit" class="login-btn">登 录</button>
        </form>
        <div class="login-footer">
          <span>默认用户名：admin</span>
          <span>默认密码：123456</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
}

.login-container {
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.login-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 40px 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.login-header h1 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-header p {
  color: #64748b;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #475569;
  font-size: 0.9rem;
}

.form-input {
  padding: 14px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #1e293b;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #6366f1;
  background: #fff;
}

.form-input::placeholder {
  color: #94a3b8;
}

.error-message {
  color: #ef4444;
  font-size: 0.85rem;
  text-align: center;
}

.login-btn {
  padding: 14px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}

.login-footer {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.login-footer span {
  color: #94a3b8;
  font-size: 0.85rem;
}
</style>
