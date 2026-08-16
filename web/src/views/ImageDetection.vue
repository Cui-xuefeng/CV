<script setup lang="ts">
import { ref } from 'vue'

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

const selectedFile = ref<File | null>(null)
const previewUrl = ref<string>('')
const resultImageUrl = ref<string>('')
const isLoading = ref(false)
const errorMsg = ref<string>('')
const selectedModel = ref('Segformer')

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0]
    previewUrl.value = URL.createObjectURL(input.files[0])
    resultImageUrl.value = ''
    errorMsg.value = ''
  }
}

const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = reader.result as string
      resolve(result)
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const handleDetect = async () => {
  if (!selectedFile.value) return

  isLoading.value = true
  errorMsg.value = ''
  resultImageUrl.value = ''

  try {
    const base64Data = await fileToBase64(selectedFile.value)
    
    const apiUrl = selectedModel.value === 'UNET' 
      ? '/local/img/detect_unet' 
      : '/local/img/detect'
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        mode: 'predict',
        image_base64: base64Data,
        save_video: false,
        model: selectedModel.value
      })
    })

    const data = await response.json()

    if (data.code === 200) {
      resultImageUrl.value = data.data.img_url
    } else {
      errorMsg.value = data.msg || '语义分割失败'
    }
  } catch (error) {
    console.error('语义分割失败:', error)
    errorMsg.value = '语义分割失败，请检查后端服务是否启动'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="detection-page">
    <div class="detection-container">
      <div class="upload-section">
        <div class="upload-area" :class="{ 'has-file': selectedFile }">
          <input
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="file-input"
            id="fileInput"
          />
          <label for="fileInput" class="upload-label">
            <template v-if="!selectedFile">
              <div class="upload-icon"></div>
              <div class="upload-text">点击选择图片或拖拽到此处</div>
              <div class="upload-hint">支持 JPG、PNG 格式</div>
            </template>
            <template v-else>
              <img :src="previewUrl" alt="预览" class="preview-image" />
            </template>
          </label>
        </div>

        <div class="model-select-wrapper">
          <label class="model-label">选择模型</label>
          <select v-model="selectedModel" class="model-select">
            <option v-for="model in models" :key="model.value" :value="model.value">
              {{ model.label }}
            </option>
          </select>
        </div>

        <button
          class="detect-btn"
          :disabled="!selectedFile || isLoading"
          @click="handleDetect"
        >
          {{ isLoading ? '分割中...' : '开始进行分割' }}
        </button>

        <div v-if="errorMsg" class="error-message">
          {{ errorMsg }}
        </div>
      </div>

      <div class="results-section" v-if="resultImageUrl">
        <h2>语义分割结果</h2>
        <div class="results-image">
          <img :src="resultImageUrl" alt="语义分割结果" class="result-image" />
        </div>
        <p class="results-hint">语义分割完成，上图为分割后的结果</p>
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
.detection-page {
  min-height: 100vh;
  background: #fff;
  color: #1e293b;
  padding-top: 100px;
}

.detection-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.upload-area {
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #6366f1;
  background: rgba(99, 102, 241, 0.05);
}

.upload-area.has-file {
  border-style: solid;
  border-color: #6366f1;
}

.file-input {
  display: none;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  cursor: pointer;
  padding: 20px;
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.upload-text {
  font-size: 1.1rem;
  color: #475569;
  margin-bottom: 10px;
}

.upload-hint {
  font-size: 0.875rem;
  color: #94a3b8;
}

.preview-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
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

.detect-btn {
  padding: 16px 40px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detect-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}

.detect-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.results-section h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #1e293b;
}

.results-image {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

.result-image {
  max-width: 100%;
  display: block;
}

.results-hint {
  color: #64748b;
  font-size: 0.9rem;
}

.error-message {
  padding: 12px 20px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 0.9rem;
}

.legend-section {
  width: 100%;
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
