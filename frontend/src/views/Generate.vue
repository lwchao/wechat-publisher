<script setup>
import { ref, reactive } from 'vue'

const form = reactive({
  keyword: '',
  title: '',
  style: 'Technical Article',
  length: 'Medium',
  model: 'glm'
})

const generating = ref(false)
const result = ref('')
const showResult = ref(false)

const styles = ['Technical Article', 'Blog Post', 'News', 'Tutorial']
const lengths = [
  { value: 'Short', label: 'Short (500-800 words)' },
  { value: 'Medium', label: 'Medium (1000-1500 words)' },
  { value: 'Long', label: 'Long (2000-3000 words)' }
]
const models = [
  { value: 'glm', label: 'GLM (Zhipu)', color: '#6366f1' },
  { value: 'qwen', label: 'Qwen (Alibaba)', color: '#f59e0b' },
  { value: 'minimax', label: 'MiniMax', color: '#22c55e' }
]

const handleSubmit = async () => {
  if (!form.keyword) {
    alert('Please enter a keyword')
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
      alert('Generation failed: ' + res.data.error)
    } else {
      result.value = res.data.content
      showResult.value = true
    }
  } catch (e) {
    alert('Generation failed: ' + e.message)
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
      alert('Save failed: ' + res.data.error)
    } else {
      alert('Saved!')
      result.value = ''
      showResult.value = false
      form.keyword = ''
      form.title = ''
    }
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

const copyContent = () => {
  navigator.clipboard.writeText(result.value)
  alert('Copied!')
}
</script>

<template>
  <div class="generate-page">
    <div class="page-header">
      <h1 class="page-title">◈ AI Generate</h1>
      <p class="page-desc">Generate articles with AI</p>
    </div>

    <div class="generate-layout">
      <!-- Form -->
      <div class="form-card">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Keyword *</label>
            <input 
              v-model="form.keyword"
              type="text" 
              placeholder="Enter topic keyword" 
              required
            />
          </div>

          <div class="form-group">
            <label>Title (optional)</label>
            <input 
              v-model="form.title"
              type="text" 
              placeholder="Custom title"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Style</label>
              <select v-model="form.style">
                <option v-for="s in styles" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>

            <div class="form-group">
              <label>Length</label>
              <select v-model="form.length">
                <option v-for="l in lengths" :key="l.value" :value="l.value">
                  {{ l.label }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Model</label>
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
            {{ generating ? '◈ Generating...' : '◈ Generate Article' }}
          </button>
        </form>
      </div>

      <!-- Result -->
      <div v-if="showResult" class="result-card">
        <div class="result-header">
          <h2>Generated Article</h2>
          <div class="result-actions">
            <button class="btn-action" @click="copyContent">📋 Copy</button>
            <button class="btn-action primary" @click="saveArticle">💾 Save</button>
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

.page-header {
  margin-bottom: 8px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.page-desc {
  color: var(--text-secondary);
  font-size: 14px;
}

.generate-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  align-items: start;
}

/* Form */
.form-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 13px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text);
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--accent);
}

.form-group input::placeholder {
  color: var(--text-muted);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* Model */
.model-selector {
  display: flex;
  gap: 8px;
}

.model-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 8px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
}

.model-option input {
  display: none;
}

.model-option:hover {
  border-color: var(--accent);
}

.model-option.active {
  border-color: var(--accent);
  background: rgba(99, 102, 241, 0.15);
  color: var(--accent);
  font-weight: 500;
}

/* Button */
.btn-generate {
  width: 100%;
  padding: 14px;
  background: var(--gradient);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
}

.btn-generate:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Result */
.result-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.result-header h2 {
  font-size: 16px;
  font-weight: 600;
}

.result-actions {
  display: flex;
  gap: 8px;
}

.btn-action {
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--border);
  background: var(--bg-tertiary);
  color: var(--text);
}

.btn-action:hover {
  border-color: var(--accent);
}

.btn-action.primary {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.result-content {
  padding: 24px;
  max-height: 600px;
  overflow-y: auto;
}

.result-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.8;
  color: var(--text-secondary);
}

@media (max-width: 900px) {
  .generate-layout {
    grid-template-columns: 1fr;
  }
}
</style>
