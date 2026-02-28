<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const stats = ref({ total: 0, drafts: 0, published: 0 })
const recentLogs = ref([])
const loading = ref(true)

const quickActions = [
  { path: '/articles', label: '文章管理', icon: '📝', color: '#07c160' },
  { path: '/generate', label: 'AI生成', icon: '✨', color: '#722ed1' },
  { path: '/git', label: 'Git操作', icon: '📦', color: '#1890ff' },
]

onMounted(async () => {
  try {
    const [articlesRes, logsRes] = await Promise.all([
      window.$api.get('/api/articles'),
      window.$api.get('/api/publish/logs')
    ])
    
    const articles = articlesRes.data || []
    stats.value = {
      total: articles.length,
      drafts: articles.filter(a => a.status === 'draft').length,
      published: articles.filter(a => a.status === 'published').length
    }
    recentLogs.value = (logsRes.data || []).slice(0, 5)
  } catch (e) {
    console.error('加载失败:', e)
  } finally {
    loading.value = false
  }
})

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}
</script>

<template>
  <div class="home">
    <!-- 欢迎卡片 -->
    <div class="welcome-card">
      <div class="welcome-content">
        <h1>欢迎使用</h1>
        <p>微信公众号发布工具 - Vue 3 重构版</p>
      </div>
      <div class="welcome-illustration">
        <span class="emoji">🚀</span>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card total">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">总文章</div>
        </div>
      </div>
      <div class="stat-card draft">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.drafts }}</div>
          <div class="stat-label">草稿</div>
        </div>
      </div>
      <div class="stat-card published">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.published }}</div>
          <div class="stat-label">已发布</div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="section">
      <h2 class="section-title">快捷操作</h2>
      <div class="actions-grid">
        <div 
          v-for="action in quickActions" 
          :key="action.path"
          class="action-card"
          :style="{ '--accent': action.color }"
          @click="router.push(action.path)"
        >
          <div class="action-icon">{{ action.icon }}</div>
          <div class="action-label">{{ action.label }}</div>
        </div>
      </div>
    </div>

    <!-- 最近发布 -->
    <div class="section">
      <h2 class="section-title">最近发布</h2>
      <div class="logs-card">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="recentLogs.length === 0" class="empty">
          暂无发布记录
        </div>
        <div v-else class="logs-list">
          <div v-for="log in recentLogs" :key="log.id" class="log-item">
            <div class="log-info">
              <span class="log-id">文章 #{{ log.article_id }}</span>
              <span :class="['log-mode', log.mode]">
                {{ log.mode === 'draft' ? '📝 草稿' : '📤 发布' }}
              </span>
            </div>
            <div class="log-time">{{ formatTime(log.published_at) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 欢迎卡片 */
.welcome-card {
  background: linear-gradient(135deg, #07c160 0%, #06ad56 100%);
  border-radius: 16px;
  padding: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  box-shadow: 0 8px 24px rgba(7, 193, 96, 0.3);
}

.welcome-content h1 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.welcome-content p {
  font-size: 14px;
  opacity: 0.9;
}

.welcome-illustration .emoji {
  font-size: 64px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 36px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #f5f5f5;
}

.stat-card.total .stat-icon { background: #e6f7ff; }
.stat-card.draft .stat-icon { background: #fffbe6; }
.stat-card.published .stat-icon { background: #f6ffed; }

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #333;
}

.stat-card.total .stat-value { color: #1890ff; }
.stat-card.draft .stat-value { color: #faad14; }
.stat-card.published .stat-value { color: #07c160; }

.stat-label {
  font-size: 14px;
  color: #666;
}

/* 区块 */
.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

/* 快捷操作 */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.action-card:hover {
  border-color: var(--accent);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.action-label {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

/* 日志卡片 */
.logs-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.logs-list {
  display: flex;
  flex-direction: column;
}

.log-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.log-item:last-child {
  border-bottom: none;
}

.log-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.log-id {
  font-weight: 500;
  color: #333;
}

.log-mode {
  font-size: 13px;
  padding: 2px 8px;
  border-radius: 4px;
  background: #f5f5f5;
}

.log-mode.draft {
  background: #fffbe6;
  color: #faad14;
}

.log-time {
  font-size: 13px;
  color: #999;
}

@media (max-width: 768px) {
  .stats-grid, .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .welcome-card {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
}
</style>
