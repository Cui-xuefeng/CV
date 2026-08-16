<script setup lang="ts">
const models = [
  { name: 'PSPNET', backbone: 'ResNet50', description: '金字塔场景解析网络，多尺度特征融合' },
  { name: 'HRNET', backbone: '宽度版本W48', description: '高分辨率网络，保持特征分辨率' },
  { name: 'UNET', backbone: '-', description: 'U型编码器解码器结构，医学影像分割' },
  { name: 'UNET3+', backbone: '-', description: 'UNET改进版，全尺度特征融合' },
  { name: 'SCHP', backbone: 'ResNet101', description: '自校正人体解析网络' },
  { name: 'DeeplabV3', backbone: 'ResNet50', description: '深度可分离卷积，空洞空间金字塔' },
  { name: 'Segformer', backbone: 'MiT-B2', description: 'Transformer架构的语义分割模型' },
  { name: 'Maskformer', backbone: 'ResNet50', description: '基于Transformer的掩码分割模型' }
]
</script>

<template>
  <div class="home">
    <section class="hero">
     
    </section>

    <section class="models-section">
      <div class="section-header">
        <h2>模型介绍</h2>
        <p>平台支持的深度学习模型</p>
      </div>
      <div class="models-grid">
        <div v-for="(model, index) in models" :key="index" class="model-card">
          <div class="model-icon">
            <span>{{ model.name.charAt(0) }}</span>
          </div>
          <div class="model-info">
            <h3>{{ model.name }}</h3>
            <div class="model-backbone">
              <span class="backbone-label">Backbone:</span>
              <span class="backbone-value">{{ model.backbone }}</span>
            </div>
            <p class="model-desc">{{ model.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: #fff;
  color: #1a1a2e;
  padding-top: 100px;
}

.hero {
  text-align: center;
  padding: 80px 20px 60px;
  background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, transparent 100%);
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 15px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  font-size: 1.1rem;
  color: #64748b;
  margin-bottom: 35px;
}

.models-section {
  padding: 60px 40px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-header h2 {
  font-size: 2rem;
  color: #1e293b;
  margin-bottom: 10px;
}

.section-header p {
  color: #64748b;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  max-width: 1200px;
  margin: 0 auto;
}

.model-card {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 25px;
  transition: all 0.3s ease;
}

.model-card:hover {
  transform: translateY(-3px);
  background: #f1f5f9;
  border-color: #6366f1;
  box-shadow: 0 10px 40px rgba(99, 102, 241, 0.15);
}

.model-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.model-icon span {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
}

.model-info {
  flex: 1;
}

.model-info h3 {
  font-size: 1.3rem;
  color: #1e293b;
  margin-bottom: 8px;
}

.model-backbone {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.backbone-label {
  font-size: 0.85rem;
  color: #94a3b8;
}

.backbone-value {
  font-size: 0.85rem;
  color: #6366f1;
  font-weight: 600;
}

.model-desc {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>
