<script setup>
import { ref, onMounted } from 'vue'

const status = ref({})
const logs = ref([])
const loading = ref(true)
const operating = ref(false)

const statusMap = {
  'M': '修改',
  'A': '新增',
  'D': '删除',
  '??': '未跟踪',
}

onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  loading.value = true
  try {
    const [statusRes, logsRes] = await Promise.all([
      window.$api.get('/api/git/status'),
      window.$api.get('/api/git/log')
    ])
    status.value = statusRes.data || {}
    logs.value = logsRes.data || []
  } catch (e) {
    console.error('加载失败:', e)
  } finally {
    loading.value = false
  }
}

const gitAdd = async () => {
  operating.value = 'add'
  try {
    const res = await window.$api.post('/api/git/add')
    if (res.data.success) {
      alert('git add 成功')
      await loadData()
    } else {
      alert('失败: ' + res.data.error)
    }
  } catch (e) {
    alert('操作失败: ' + e.message)
  } finally {
    operating.value = false
  }
}

const gitCommit = async () => {
  const message = prompt('请输入提交信息:')
  if (!message) return
  
  operating.value = 'commit'
  try {
    const res = await window.$api.post('/api/git/commit', { message })
    if (res.data.success) {
      alert('提交成功')
      await loadData()
    } else {
      alert('失败: ' + res.data.error)
    }
  } catch (e) {
    alert('操作失败: ' + e.message)
  } finally {
    operating.value = false
  }
}

const gitPush = async () => {
  operating.value = 'push'
  try {
    const res = await window.$api.post('/api/git/push')
    if (res.data.success) {
      alert('推送成功')
    } else {
      alert('失败: ' + res.data.error)
    }
  } catch (e) {
    alert('操作失败: ' + e.message)
  } finally {
    operating.value = false
  }
}

const gitPull = async () => {
  operating.value = 'pull'
  try {
    const res = await window.$api.post('/api/git/pull')
    if (res.data.success) {
      alert('拉取成功')
      await loadData()
    } else {
      alert('失败: ' + res.data.error)
    }
  } catch (e) {
    alert('操作失败: ' + e.message)
  } finally {
    operating.value = false
  }
}
</script>

<template>
  <div class="git-page">
    <div class="page-header">
      <h1>📦 Git 操作</h1>
    </div>

    <div class="git-layout">
      <!-- 状态卡片 -->
      <div class="status-card">
        <h2>仓库状态</h2>
        
        <div v-if="loading" class="loading">加载中...</div>
        
        <div v-else class="status-info">
          <div class="status-row">
            <span class="label">当前分支</span>
            <span class="value branch">{{ status.branch || '未知' }}</span>
          </div>
          
          <div class="status-row">
            <span class="label">工作区</span>
            <span :class="['value', status.clean ? 'clean' : 'dirty']">
              {{ status.clean ? '✅ 清洁' : '⚠️ 有更改' }}
            </span>
          </div>
          
          <!-- 文件列表 -->
          <div v-if="status.files?.length" class="files-section">
            <h3>更改的文件 ({{ status.files.length }})</h3>
            <div class="files-list">
              <div 
                v-for="file in status.files" 
                :key="file.file"
                class="file-item"
              >
                <span class="file-status">{{ statusMap[file.status] || file.status }}</span>
                <span class="file-name">{{ file.file }}</span>
              </div>
            </div>
          </div>
          
          <div v-else-if="status.clean" class="clean-state">
            ✅ 工作区清洁，没有需要提交的更改
          </div>
        </div>
      </div>

      <!-- 操作卡片 -->
      <div class="operations-card">
        <h2>操作</h2>
        
        <div class="ops-grid">
          <button 
            class="op-btn add"
            :disabled="operating"
            @click="gitAdd"
          >
            <span class="op-icon">➕</span>
            <span class="op-label">git add .</span>
          </button>
          
          <button 
            class="op-btn commit"
            :disabled="operating"
            @click="gitCommit"
          >
            <span class="op-icon">📝</span>
            <span class="op-label">git commit</span>
          </button>
          
          <button 
            class="op-btn pull"
            :disabled="operating"
            @click="gitPull"
          >
            <span class="op-icon">⬇️</span>
            <span class="op-label">git pull</span>
          </button>
          
          <button 
            class="op-btn push"
            :disabled="operating"
            @click="gitPush"
          >
            <span class="op-icon">⬆️</span>
            <span class="op-label">git push</span>
          </button>
        </div>
      </div>

      <!-- 提交历史 -->
      <div class="logs-card">
        <h2>提交历史</h2>
        
        <div v-if="loading" class="loading">加载中...</div>
        
        <div v-else-if="logs.length === 0" class="empty">
          暂无提交记录
        </div>
        
        <div v-else class="logs-list">
          <div v-for="log in logs" :key="log.hash" class="log-item">
            <div class="log-hash">{{ log.hash }}</div>
            <div class="log-info">
              <div class="log-message">{{ log.message }}</div>
              <div class="log-meta">
                <span class="log-author">{{ log.author }}</span>
                <span class="log-date">{{ log.date?.split(' ')[0] }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.git-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.git-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.status-card, .operations-card, .logs-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.logs-card {
  grid-column: 1 / -1;
}

h2 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

/* 状态 */
.status-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.status-row .label {
  color: #666;
}

.status-row .value {
  font-weight: 600;
}

.value.branch {
  color: #1890ff;
}

.value.clean {
  color: #07c160;
}

.value.dirty {
  color: #faad14;
}

/* 文件列表 */
.files-section {
  margin-top: 16px;
}

.files-section h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.files-list {
  max-height: 200px;
  overflow-y: auto;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}

.file-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  background: #f0f5ff;
  color: #1890ff;
}

.file-name {
  font-size: 13px;
  color: #333;
  font-family: monospace;
}

.clean-state {
  margin-top: 16px;
  padding: 16px;
  background: #f6ffed;
  border-radius: 8px;
  color: #07c160;
  text-align: center;
}

/* 操作按钮 */
.ops-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.op-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.op-btn:hover:not(:disabled) {
  border-color: #07c160;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(7, 193, 96, 0.15);
}

.op-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.op-icon {
  font-size: 24px;
}

.op-label {
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

/* 提交历史 */
.logs-list {
  max-height: 300px;
  overflow-y: auto;
}

.log-item {
  display: flex;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.log-item:last-child {
  border-bottom: none;
}

.log-hash {
  font-family: monospace;
  font-size: 13px;
  color: #1890ff;
  background: #e6f7ff;
  padding: 4px 8px;
  border-radius: 4px;
  height: fit-content;
}

.log-message {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.log-meta {
  font-size: 12px;
  color: #999;
}

.log-author {
  margin-right: 12px;
}

@media (max-width: 768px) {
  .git-layout {
    grid-template-columns: 1fr;
  }
  
  .ops-grid {
    grid-template-columns: 1fr;
  }
}
</style>
