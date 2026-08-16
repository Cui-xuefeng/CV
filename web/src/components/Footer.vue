<script setup lang="ts">
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h4>语义分割平台</h4>
          <p>基于深度学习的图像语义分割解决方案</p>
        </div>
        <div class="footer-section">
          <h4>快速链接</h4>
          <ul>
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/image-detection">图像检测</router-link></li>
            <li><router-link to="/realtime-detection">实时检测</router-link></li>
          </ul>
        </div>
        <div class="footer-section">
          <h4>联系方式</h4>
          <p>邮箱：support@example.com</p>
          <p>电话：400-123-4567</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 语义分割平台. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #fff;
  border-top: 1px solid #e2e8f0;
  padding: 40px 0 20px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.footer-section h4 {
  color: #1e293b;
  margin-bottom: 15px;
  font-size: 1rem;
}

.footer-section p {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.footer-section ul li a {
  color: #64748b;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.footer-section ul li a:hover {
  color: #6366f1;
}

.footer-bottom {
  border-top: 1px solid #e2e8f0;
  padding-top: 20px;
  text-align: center;
}

.footer-bottom p {
  color: #94a3b8;
  font-size: 0.85rem;
}
</style>
