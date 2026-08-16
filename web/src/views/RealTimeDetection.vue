<script setup lang="ts">
import { ref, onUnmounted } from 'vue'

const models = [
  { value: 'PSPNET', label: 'PSPNET' },
  { value: 'HRNET', label: 'HRNET' },
  { value: 'UNET', label: 'UNET' },
  { value: 'UNET3+', label: 'UNET3+' },
  { value: 'SCHP', label: 'SCHP' },
  { value: 'DeeplabV3', label: 'DeeplabV3' },
  { value: 'Segformer', label: 'Segformer' },
  { value: 'Maskformer', label: 'Maskformer' }
]

const videoRef = ref<HTMLImageElement | null>(null)
const isStreaming = ref(false)
const isLoading = ref(false)
const errorMsg = ref<string>('')
const videoFeedUrl = ref<string>('')
const selectedModel = ref('Segformer')

const startDetection = async () => {
  try {
    isLoading.value = true
    errorMsg.value = ''

    const response = await fetch('/local/detect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        mode: 'video',
        save_video: true,
        model: selectedModel.value
      })
    })

    const data = await response.json()

    if (data.code === 200) {
      videoFeedUrl.value = '/local/video_feed'
      isStreaming.value = true
    } else {
      errorMsg.value = data.msg || '启动语义分割失败'
    }
  } catch (error) {
    console.error('启动语义分割失败:', error)
    errorMsg.value = '启动语义分割失败，请检查后端服务是否启动'
  } finally {
    isLoading.value = false
  }
}

const stopDetection = async () => {
  try {
    const response = await fetch('/local/stop_detect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (data.code === 200) {
      isStreaming.value = false
      videoFeedUrl.value = ''
    } else {
      errorMsg.value = data.msg || '停止语义分割失败'
    }
  } catch (error) {
    console.error('停止语义分割失败:', error)
    errorMsg.value = '停止语义分割失败'
  }
}

onUnmounted(() => {
  if (isStreaming.value) {
    stopDetection()
  }
})
</script>

<template>
  <div class="realtime-page">
    <div class="camera-container">
      <div class="video-wrapper">
        <img 
          v-if="isStreaming && videoFeedUrl" 
          :src="videoFeedUrl" 
          ref="videoRef"
          class="video-element"
          alt="实时语义分割视频流"
        />

        <div v-if="!isStreaming && !isLoading" class="camera-placeholder">
          <div class="placeholder-content">
            <div class="camera-icon"></div>
            <p>点击下方按钮启动实时语义分割</p>
          </div>
        </div>

        <div v-if="isLoading" class="camera-loading">
          <div class="spinner"></div>
          <p>正在启动语义分割...</p>
        </div>

        <div v-if="errorMsg" class="error-message">
          {{ errorMsg }}
        </div>
      </div>

      <div class="controls">
        <div class="model-select-wrapper">
          <label class="model-label">选择模型</label>
          <select v-model="selectedModel" class="model-select" :disabled="isStreaming">
            <option v-for="model in models" :key="model.value" :value="model.value">
              {{ model.label }}
            </option>
          </select>
        </div>
        <button v-if="!isStreaming" class="control-btn start-btn" @click="startDetection" :disabled="isLoading">
          {{ isLoading ? '启动中...' : '启动分割' }}
        </button>
        <button v-else class="control-btn stop-btn" @click="stopDetection">
          停止语义分割
        </button>
      </div>

      <div v-if="isStreaming" class="detection-info">
        <div class="info-item">
          <span class="info-label">检测状态</span>
          <span class="info-value status-active">● 实时检测中</span>
        </div>
        <div class="info-item">
          <span class="info-label">视频流</span>
          <span class="info-value">MJPEG</span>
        </div>
        <div class="info-item">
          <span class="info-label">当前模型</span>
          <span class="info-value">{{ selectedModel }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">后端服务</span>
          <span class="info-value">运行中</span>
        </div>
      </div>

      <div class="legend-section">
        <h3>颜色图例</h3>
        <div class="legend-grid">
          <div class="legend-item">
            <span class="legend-color" style="background: #000000;"></span>
            <span class="legend-label">背景</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #8B4513;"></span>
            <span class="legend-label">飞机</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #008000;"></span>
            <span class="legend-label">自行车</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #808000;"></span>
            <span class="legend-label">鸟</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #00008B;"></span>
            <span class="legend-label">船</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #800080;"></span>
            <span class="legend-label">瓶子</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #4169E1;"></span>
            <span class="legend-label">公交车</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #808080;"></span>
            <span class="legend-label">小汽车</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #8B0000;"></span>
            <span class="legend-label">猫</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #B22222;"></span>
            <span class="legend-label">椅子</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #556B2F;"></span>
            <span class="legend-label">牛</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #CD853F;"></span>
            <span class="legend-label">餐桌</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #483D8B;"></span>
            <span class="legend-label">狗</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #FF69B4;"></span>
            <span class="legend-label">马</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #708090;"></span>
            <span class="legend-label">摩托车</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #BC8F8F;"></span>
            <span class="legend-label">人</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #006400;"></span>
            <span class="legend-label">盆栽</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #A0522D;"></span>
            <span class="legend-label">羊</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #7CFC00;"></span>
            <span class="legend-label">沙发</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #ADFF2F;"></span>
            <span class="legend-label">火车</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: #006994;"></span>
            <span class="legend-label">显示器</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.realtime-page {
  min-height: 100vh;
  background: #fff;
  color: #1e293b;
  padding-top: 100px;
}

.camera-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px;
}

.video-wrapper {
  position: relative;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 16 / 9;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.camera-placeholder,
.camera-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(248, 250, 252, 0.95);
}

.placeholder-content {
  text-align: center;
}

.camera-icon {
  font-size: 5rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.placeholder-content p {
  color: #64748b;
  font-size: 1.1rem;
}

.camera-loading {
  flex-direction: column;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(99, 102, 241, 0.3);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.camera-loading p {
  color: #64748b;
}

.error-message {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 20px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.9rem;
  max-width: 80%;
  text-align: center;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.model-select-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.model-label {
  font-size: 0.95rem;
  color: #475569;
  font-weight: 500;
}

.model-select {
  padding: 10px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  color: #1e293b;
  background: #fff;
  cursor: pointer;
  min-width: 150px;
}

.model-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.model-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.control-btn {
  padding: 16px 50px;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
}

.start-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}

.start-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stop-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #fff;
}

.stop-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
}

.detection-info {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 30px;
  padding: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.info-label {
  font-size: 0.875rem;
  color: #94a3b8;
}

.info-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
}

.status-active {
  color: #22c55e;
}

.legend-section {
  margin-top: 30px;
  padding: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.legend-section h3 {
  margin-bottom: 15px;
  font-size: 1.1rem;
  color: #1e293b;
  text-align: center;
}

.legend-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

@media (max-width: 600px) {
  .legend-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-color {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  flex-shrink: 0;
}

.legend-label {
  font-size: 0.9rem;
  color: #475569;
}
</style>
