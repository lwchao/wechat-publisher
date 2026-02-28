<script setup>
import { ref, onMounted } from 'vue'

const articles = ref([])
const loading = ref(true)
const publishing = ref(null)

const statusMap = {
  draft: { label: '草稿', class: 'draft' },
  published: { label: '已发布', class: 'published' }
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
  if (!confirm('确定要发布这篇文章吗？')) return
  
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
  if (!confirm('确定要删除这篇文章吗？')) return
  
  try {
    await window.$api.delete(`/api/articles/${id}`)
    await loadArticles()
  } catch (e) {
    alert('删除失败: ' + e.message)
  }
}

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}
</script>

<template>
  <div class="articles-page">
    <div class="page-header">
      <h1>文章管理</h1>
      <button class="btn-primary" @click="$router.push('/generate')">
        <span>✨</span> AI生成
      </button>
    </div>

    <div class="articles-card">
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="articles.length === 0" class="empty">
        <div class="empty-icon">📝</div>
        <p>暂无文章</p>
        <button class="btn-primary" @click="$router.push('/generate')">
          立即创建
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
                  {{ publishing === article.id ? '发布中...' : '发布' }}
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
  align-items: center;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #07c160 0%, #06ad56 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(7, 193, 96, 0.3);
}

.articles-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.loading, .empty {
  text-align: center;
  padding: 60px 20px;
  color: #999;
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
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.articles-table th {
  background: #fafafa;
  font-weight: 600;
  color: #666;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.articles-table tbody tr:hover {
  background: #fafafa;
}

.title-cell .title {
  font-weight: 500;
  color: #333;
}

.category {
  display: inline-block;
  padding: 2px 10px;
  background: #f0f5ff;
  color: #1890ff;
  border-radius: 4px;
  font-size: 13px;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.status-badge.draft {
  background: #fffbe6;
  color: #faad14;
}

.status-badge.published {
  background: #f6ffed;
  color: #07c160;
}

.time {
  color: #999;
  font-size: 13px;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-publish, .btn-delete {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-publish {
  background: #07c160;
  color: white;
}

.btn-publish:hover:not(:disabled) {
  background: #06ad56;
}

.btn-publish:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-delete {
  background: #fff1f0;
  color: #ff4d4f;
}

.btn-delete:hover {
  background: #ffccc7;
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
