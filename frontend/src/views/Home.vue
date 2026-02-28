<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const stats = ref({ total: 0, drafts: 0, published: 0 })
const recentLogs = ref([])
const loading = ref(true)

const features = [
  { title: 'AI Writing', desc: 'Generate articles with AI', icon: '◈', link: '/generate', color: '#6366f1' },
  { title: 'Article Management', desc: 'Manage your content', icon: '◎', link: '/articles', color: '#22c55e' },
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
    console.error('Load failed:', e)
  } finally {
    loading.value = false
  }
})

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          Better articles,<br/>
          <span class="gradient-text">better publishing</span>
        </h1>
        <p class="hero-desc">
          AI-powered WeChat article generation and publishing. 
          Write, generate, and publish — all in one place.
        </p>
        <div class="hero-actions">
          <button class="btn-primary" @click="router.push('/generate')">
            <span>◈</span> Start Generating
          </button>
          <button class="btn-secondary" @click="router.push('/articles')">
            <span>◎</span> View Articles
          </button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="visual-card">
          <div class="card-header">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
          </div>
          <pre class="code-block"># AI Generated Article

## Introduction
Lorem ipsum dolor sit amet...

## Main Content
More engaging content here...

## Conclusion
Thanks for reading!</pre>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-section">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(99, 102, 241, 0.15); color: #6366f1;">◉</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">Total Articles</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b;">◎</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.drafts }}</div>
          <div class="stat-label">Drafts</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(34, 197, 94, 0.15); color: #22c55e;">✓</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.published }}</div>
          <div class="stat-label">Published</div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features-section">
      <h2 class="section-title">Features</h2>
      <div class="features-grid">
        <div 
          v-for="f in features" 
          :key="f.title"
          class="feature-card"
          @click="router.push(f.link)"
        >
          <div class="feature-icon" :style="{ background: f.color + '20', color: f.color }">
            {{ f.icon }}
          </div>
          <h3 class="feature-title">{{ f.title }}</h3>
          <p class="feature-desc">{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Recent Activity -->
    <section class="activity-section">
      <h2 class="section-title">Recent Activity</h2>
      <div class="activity-card">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="recentLogs.length === 0" class="empty">No recent activity</div>
        <div v-else class="activity-list">
          <div v-for="log in recentLogs" :key="log.id" class="activity-item">
            <div class="activity-info">
              <span class="activity-id">#{{ log.article_id }}</span>
              <span :class="['activity-mode', log.mode]">
                {{ log.mode === 'draft' ? '📝 Draft' : '📤 Published' }}
              </span>
            </div>
            <span class="activity-time">{{ formatTime(log.published_at) }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

/* Hero */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
  padding: 32px 0;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
  margin-bottom: 20px;
}

.gradient-text {
  background: var(--gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 32px;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.btn-primary, .btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background: var(--gradient);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  border-color: var(--border-light);
  background: var(--border);
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.visual-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  width: 100%;
  max-width: 400px;
}

.card-header {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ef4444; }
.dot.yellow { background: #f59e0b; }
.dot.green { background: #22c55e; }

.code-block {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.8;
}

/* Stats */
.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--border-light);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Section */
.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
}

/* Features */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.feature-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.feature-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.feature-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.feature-desc {
  font-size: 14px;
  color: var(--text-secondary);
}

/* Activity */
.activity-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
}

.activity-list {
  display: flex;
  flex-direction: column;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.activity-id {
  font-weight: 500;
}

.activity-mode {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--bg-tertiary);
}

.activity-mode.draft {
  color: #f59e0b;
}

.activity-time {
  font-size: 13px;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-title {
    font-size: 32px;
  }
  
  .hero-desc {
    max-width: 100%;
  }
  
  .hero-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .stats-section, .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
