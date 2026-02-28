<script setup>
import { ref, onMounted } from 'vue'

const articles = ref([])
const loading = ref(true)
const publishing = ref(null)

const statusMap = {
  draft: { label: '草稿', class: 'draft' },
  published: { label: '已发布', class: 'published' }
}
  draft: { label: 'Draft', class: 'draft' },
  published: { label: 'Published', class: 'published' }
}

onMounted(async () => {
  await loadArticles()
})

const loadArticles = async () => {
  loading.value = true
  try {
    const res = await window.$api.get('/api/articles')
    articles.value = res.data || []
  } catch (e) {
    console.error('加载失败:', e)
  } finally {
    loading.value = false
  }
}

const publishArticle = async (id) => {
  if (!confirm('确定发布这篇文章?')) return
  
  publishing.value = id
  try {
    const res = await window.$api.post('/api/publish', {
      article_id: id,
      draft_mode: false
    })
    
    if (res.data.error) {
      alert('发布失败: ' + res.data.error)
    } else {
      alert('发布成功!')
      await loadArticles()
    }
  } catch (e) {
    alert('发布失败: ' + e.message)
  } finally {
    publishing.value = null
  }
}

const deleteArticle = async (id) => {
  if (!confirm('确定删除这篇文章?')) return
  
  try {
    await window.$api.delete(`/api/articles/${id}`)
    await loadArticles()
  } catch (e) {
    alert('删除失败: ' + e.message)
  }
}

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <div class="articles-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">文章</h1>
        <p class="page-desc">管理您的发布内容</p>
        <p class="page-desc">Manage your published content</p>
      </div>
      <button class="btn-primary" @click="$router.push('/generate')">
        <span>◈</span> 新建文章
      </button>
    </div>

    <div class="articles-card">
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="articles.length === 0" class="empty">
        <div class="empty-icon">◎</div>
        <p>暂无文章</p>
        <button class="btn-primary" @click="$router.push('/generate')">
          创建第一篇文章
        </button>
      </div>
      
      <table v-else class="articles-table">
        <thead>
          <tr>
            <th>标题</th>
            <th>作者</th>
            <th>分类</th>
            <th>状态</th>
            <th>更新时间</th>
            <th>操作</th>
            <th>Author</th>
            <th>Category</th>
            <th>Status</th>
            <th>Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articles" :key="article.id">
            <td class="title-cell">
              <span class="title">{{ article.title }}</span>
            </td>
            <td>{{ article.author }}</td>
            <td>
              <span class="category">{{ article.category }}</span>
            </td>
            <td>
              <span :class="['status-badge', statusMap[article.status]?.class]">
                {{ statusMap[article.status]?.label || article.status }}
              </span>
            </td>
            <td class="time">{{ formatTime(article.updated_at) }}</td>
            <td>
              <div class="actions">
                <button 
                  class="btn-publish"
                  :disabled="publishing === article.id || article.status === 'published'"
                  @click="publishArticle(article.id)"
                >
                  {{ publishing === article.id ? '...' : '发布' }}
                </button>
                <button 
                  class="btn-delete"
                  @click="deleteArticle(article.id)"
                >
                  删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.articles-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--gradient);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
}

.articles-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.loading, .empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty p {
  margin-bottom: 20px;
  font-size: 15px;
}

.articles-table {
  width: 100%;
  border-collapse: collapse;
}

.articles-table th,
.articles-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.articles-table th {
  background: var(--bg-tertiary);
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.articles-table tbody tr:hover {
  background: var(--bg-tertiary);
}

.title-cell .title {
  font-weight: 500;
}

.category {
  display: inline-block;
  padding: 2px 10px;
  background: rgba(99, 102, 241, 0.15);
  color: #6366f1;
  border-radius: 4px;
  font-size: 12px;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.draft {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.status-badge.published {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.time {
  color: var(--text-secondary);
  font-size: 13px;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-publish, .btn-delete {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-publish {
  background: var(--accent);
  color: white;
}

.btn-publish:hover:not(:disabled) {
  background: var(--accent-hover);
}

.btn-publish:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-delete {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.25);
}

@media (max-width: 768px) {
  .articles-table th:nth-child(2),
  .articles-table td:nth-child(2),
  .articles-table th:nth-child(3),
  .articles-table td:nth-child(3) {
    display: none;
  }
}
</style>
