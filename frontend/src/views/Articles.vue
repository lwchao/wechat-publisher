<script setup>
import { ref, onMounted } from 'vue'

const articles = ref([])
const loading = ref(true)
const publishing = ref(null)

const statusMap = {
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
    console.error('Load failed:', e)
  } finally {
    loading.value = false
  }
}

const publishArticle = async (id) => {
  if (!confirm('Publish this article?')) return
  
  publishing.value = id
  try {
    const res = await window.$api.post('/api/publish', {
      article_id: id,
      draft_mode: false
    })
    
    if (res.data.error) {
      alert('Publish failed: ' + res.data.error)
    } else {
      alert('Published!')
      await loadArticles()
    }
  } catch (e) {
    alert('Publish failed: ' + e.message)
  } finally {
    publishing.value = null
  }
}

const deleteArticle = async (id) => {
  if (!confirm('Delete this article?')) return
  
  try {
    await window.$api.delete(`/api/articles/${id}`)
    await loadArticles()
  } catch (e) {
    alert('Delete failed: ' + e.message)
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
        <h1 class="page-title">Articles</h1>
        <p class="page-desc">Manage your published content</p>
      </div>
      <button class="btn-primary" @click="$router.push('/generate')">
        <span>◈</span> New Article
      </button>
    </div>

    <div class="articles-card">
      <div v-if="loading" class="loading">Loading...</div>
      
      <div v-else-if="articles.length === 0" class="empty">
        <div class="empty-icon">◎</div>
        <p>No articles yet</p>
        <button class="btn-primary" @click="$router.push('/generate')">
          Create your first article
        </button>
      </div>
      
      <table v-else class="articles-table">
        <thead>
          <tr>
            <th>Title</th>
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
                  {{ publishing === article.id ? '...' : 'Publish' }}
                </button>
                <button 
                  class="btn-delete"
                  @click="deleteArticle(article.id)"
                >
                  Delete
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
