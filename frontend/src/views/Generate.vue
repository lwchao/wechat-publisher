<script setup>
import { ref, reactive } from 'vue'

const form = reactive({
  keyword: '',
  title: '',
  style: '技术文章',
  length: '中等',
  model: 'glm'
})

const generating = ref(false)
const result = ref('')
const showResult = ref(false)

const styles = ['技术文章', '科普', '生活', '商业']
const lengths = [
  { value: '短', label: '短 (500-800字)' },
  { value: '中等', label: '中等 (1000-1500字)' },
  { value: '长', label: '长 (2000-3000字)' }
]
const models = [
  { value: 'glm', label: '智谱 GLM' },
  { value: 'minimax', label: 'MiniMax' },
  { value: 'qwen', label: '通义千问' }
]

const handleSubmit = async () => {
  if (!form.keyword) {
    alert('请输入关键词')
    return
  }
  
  generating.value = true
  showResult.value = false
  
  try {
    const res = await window.$api.post('/api/ai/generate', {
      keyword: form.keyword,
      title: form.title || undefined,
      style: form.style,
      length: form.length,
      model: form.model
    })
    
    if (res.data.error) {
      alert('生成失败: ' + res.data.error)
    } else {
      result.value = res.data.content
      showResult.value = true
    }
  } catch (e) {
    alert('生成失败: ' + e.message)
  } finally {
    generating.value = false
  }
}

const saveArticle = async () => {
  try {
    const res = await window.$api.post('/api/ai/save', {
      content: result.value,
      keyword: form.keyword,
      title: form.title || undefined
    })
    
    if (res.data.error) {
      alert('保存失败: ' + res.data.error)
    } else {
      alert('保存成功！')
      result.value = ''
      showResult.value = false
      form.keyword = ''
      form.title = ''
    }
  } catch (e) {
    alert('保存失败: ' + e.message)
  }
}

const copyContent = () => {
  navigator.clipboard.writeText(result.value)
  alert('已复制到剪贴板')
}
</script>

<template>
  <div class="generate-page">
    <div class="page-header">
      <h1>✨ AI 生成文章</h1>
    </div>

    <div class="generate-layout">
      <!-- 表单 -->
      <div class="form-card">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>关键词 *</label>
            <input 
              v-model="form.keyword"
              type="text" 
              placeholder="输入文章主题关键词" 
              required
            />
          </div>

          <div class="form-group">
            <label>文章标题（可选）</label>
            <input 
              v-model="form.title"
              type="text" 
              placeholder="留空则自动生成"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>文章风格</label>
              <select v-model="form.style">
                <option v-for="s in styles" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>

            <div class="form-group">
              <label>文章长度</label>
              <select v-model="form.length">
                <option v-for="l in lengths" :key="l.value" :value="l.value">
                  {{ l.label }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>AI 模型</label>
            <div class="model-selector">
              <label 
                v-for="m in models" 
                :key="m.value"
                class="model-option"
                :class="{ active: form.model === m.value }"
              >
                <input 
                  v-model="form.model" 
                  type="radio" 
                  :value="m.value"
                />
                {{ m.label }}
              </label>
            </div>
          </div>

          <button 
            type="submit" 
            class="btn-generate"
            :disabled="generating"
          >
            {{ generating ? '🤔 生成中...' : '✨ 开始生成' }}
          </button>
        </form>
      </div>

      <!-- 结果 -->
      <div v-if="showResult" class="result-card">
        <div class="result-header">
          <h2>生成结果</h2>
          <div class="result-actions">
            <button class="btn-action" @click="copyContent">📋 复制</button>
            <button class="btn-action primary" @click="saveArticle">💾 保存</button>
          </div>
        </div>
        <div class="result-content">
          <pre>{{ result }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.generate-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.generate-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  align-items: start;
}

/* 表单卡片 */
.form-card {
  background: white;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #07c160;
  box-shadow: 0 0 0 3px rgba(7, 193, 96, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* 模型选择 */
.model-selector {
  display: flex;
  gap: 12px;
}

.model-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.model-option input {
  display: none;
}

.model-option:hover {
  border-color: #07c160;
}

.model-option.active {
  border-color: #07c160;
  background: #f6ffed;
  color: #07c160;
  font-weight: 500;
}

/* 生成按钮 */
.btn-generate {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #722ed1 0%, #531dab 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(114, 46, 209, 0.3);
}

.btn-generate:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 结果卡片 */
.result-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.result-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.result-actions {
  display: flex;
  gap: 12px;
}

.btn-action {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #d9d9d9;
  background: white;
}

.btn-action:hover {
  border-color: #07c160;
  color: #07c160;
}

.btn-action.primary {
  background: #07c160;
  color: white;
  border-color: #07c160;
}

.btn-action.primary:hover {
  background: #06ad56;
}

.result-content {
  padding: 24px;
  max-height: 600px;
  overflow-y: auto;
}

.result-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.8;
  color: #333;
}

@media (max-width: 900px) {
  .generate-layout {
    grid-template-columns: 1fr;
  }
}
</style>
