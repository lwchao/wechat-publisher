<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/', label: 'Home', icon: '⬡' },
  { path: '/articles', label: 'Articles', icon: '◎' },
  { path: '/generate', label: 'Generate', icon: '◈' },
]
</script>

<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="header-inner">
        <a href="/" class="logo">
          <span class="logo-icon">◉</span>
          <span class="logo-text">WeChat Publisher</span>
        </a>
        
        <nav class="nav">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ active: route.path === item.path }"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            {{ item.label }}
          </router-link>
        </nav>
        
        <div class="header-right">
          <a href="https://github.com/lwchao/wechat-publisher" target="_blank" class="github-link">
            GitHub
          </a>
        </div>
      </div>
    </header>

    <!-- Main -->
    <main class="main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <p>WeChat Publisher © 2026 — Open source AI-powered publishing tool</p>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg: #f8f9fa;
  --bg-secondary: #ffffff;
  --bg-tertiary: #f0f2f5;
  --border: #e5e7eb;
  --border-light: #d1d5db;
  --text: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --accent: #6366f1;
  --accent-hover: #4f46e5;
  --accent-bg: #eef2ff;
  --success: #22c55e;
  --warning: #f59e0b;
  --error: #ef4444;
  --gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

body {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.header-inner {
  max-width: 1200px;
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
  text-decoration: none;
  color: var(--text);
}

.logo-icon {
  font-size: 24px;
  color: var(--accent);
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.nav {
  display: flex;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--text);
  background: var(--bg-tertiary);
}

.nav-link.active {
  color: var(--accent);
  background: var(--accent-bg);
}

.nav-icon {
  font-size: 16px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.github-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border);
  transition: all 0.2s ease;
}

.github-link:hover {
  color: var(--text);
  border-color: var(--border-light);
  background: var(--bg-tertiary);
}

/* Main */
.main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 24px;
}

/* Footer */
.footer {
  border-top: 1px solid var(--border);
  padding: 24px;
  text-align: center;
}

.footer p {
  color: var(--text-muted);
  font-size: 13px;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg);
}

::-webkit-scrollbar-thumb {
  background: var(--border-light);
  border-radius: 4px;
#TK|
#TM|::-webkit-scrollbar-thumb:hover {
#WY|  background: #9ca3af;
#PP|}
#HB|

::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
  background: #444;
}

@media (max-width: 768px) {
  .header-inner {
    padding: 0 16px;
  }
  
  .logo-text {
    display: none;
  }
  
  .nav-link {
    padding: 8px 12px;
  }
  
  .nav-link span:not(.nav-icon) {
    display: none;
  }
  
  .main {
    padding: 24px 16px;
  }
}
</style>
