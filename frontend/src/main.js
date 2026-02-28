import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import App from './App.vue'
import './style.css'

// 配置 API 基础 URL
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

// 路由配置
const routes = [
  { path: '/', name: 'Home', component: () => import('./views/Home.vue') },
  { path: '/articles', name: 'Articles', component: () => import('./views/Articles.vue') },
  { path: '/generate', name: 'Generate', component: () => import('./views/Generate.vue') },
]
const routes = [
  { path: '/', name: 'Home', component: () => import('./views/Home.vue') },
  { path: '/articles', name: 'Articles', component: () => import('./views/Articles.vue') },
  { path: '/generate', name: 'Generate', component: () => import('./views/Generate.vue') },
  { path: '/git', name: 'Git', component: () => import('./views/Git.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.config.globalProperties.$api = api
app.use(router)
app.mount('#app')
