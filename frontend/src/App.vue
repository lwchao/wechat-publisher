<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const currentTime = ref('')

const navItems = [
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/articles', label: '文章', icon: '📝' },
  { path: '/generate', label: 'AI生成', icon: '✨' },
]
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/articles', label: '文章', icon: '📝' },
  { path: '/generate', label: 'AI生成', icon: '✨' },
  { path: '/git', label: 'Git', icon: '📦' },
]

onMounted(() => {
  const updateTime = () => {
    currentTime.value = new Date().toLocaleString('zh-CN')
  }
  updateTime()
  setInterval(updateTime, 1000)
})
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">📱</span>
          <span class="logo-text">微信公众号发布工具</span>
        </div>
        <nav class="nav">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: route.path === item.path }"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </nav>
        <div class="header-right">
          <span class="time">{{ currentTime }}</span>
        </div>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>© 2026 微信公众号发布工具 - Powered by Vue 3 + Flask</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

/* 头部 */
.header {
  background: linear-gradient(135deg, #07c160 0%, #06ad56 100%);
  box-shadow: 0 2px 12px rgba(7, 193, 96, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: white;
  letter-spacing: 0.5px;
}

/* 导航 */
.nav {
  display: flex;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  font-size: 16px;
}

.nav-label {
  font-size: 14px;
}

.header-right {
  color: rgba(255, 255, 255, 0.85);
  font-size: 13px;
}

/* 主内容 */
.main-content {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 24px;
}

/* 页脚 */
.footer {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 13px;
  background: white;
  border-top: 1px solid #eee;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .logo-text {
    display: none;
  }
  
  .nav-label {
    display: none;
  }
  
  .nav-item {
    padding: 8px 12px;
  }
  
  .main-content {
    padding: 16px;
  }
}
</style>
