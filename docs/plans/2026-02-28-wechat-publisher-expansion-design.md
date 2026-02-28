# 微信公众号发布工具扩展设计

**日期**: 2026-02-28
**项目**: wechat-publisher 扩展功能

---

## 1. 需求概述

扩展现有微信公众号发布工具，增加以下功能：
- 自动提交 GitHub（Webhook + 本地脚本 + 定时 + 手动）
- Web 界面（文章管理 + 发布控制 + Git 操作 + AI 生成）
- 根据关键词自动生成公众号 Markdown 文档

---

## 2. 架构设计

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────┐
│                    Web 界面                          │
│  (文章管理 / 发布控制 / Git操作 / AI生成)            │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                  Flask API Server                    │
│  - /api/articles    (文章 CRUD)                     │
│  - /api/publish     (发布控制)                      │
│  - /api/git         (Git 操作)                      │
│  - /api/ai/generate (AI 生成)                       │
│  - /api/webhook/github (GitHub Webhook)            │
│  - /api/scheduler   (定时任务)                      │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                  SQLite 数据库                       │
│  - articles (文章表)                                │
│  - publish_logs (发布记录)                          │
│  - config (配置)                                    │
└─────────────────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│              Python CLI (原有 + 扩展)                │
│  - wechat_publisher.py                             │
│  - git_helper.py                                    │
│  - ai_writer.py                                     │
└─────────────────────────────────────────────────────┘
```

### 2.2 目录结构

```
wechat-publisher/
├── app.py                    # Flask 主应用
├── database.py               # SQLite 操作
├── models.py                 # 数据模型
├── api/
│   ├── __init__.py
│   ├── articles.py           # 文章 API
│   ├── publish.py            # 发布 API
│   ├── git_ops.py            # Git 操作 API
│   ├── ai_gen.py             # AI 生成 API
│   └── webhook.py           # Webhook 处理
├── scheduler.py              # 定时任务
├── git_helper.py             # Git 辅助脚本
├── ai_writer.py              # AI 写作模块
├── wechat_publisher.py       # 原有代码
├── templates/
│   ├── base.html            # 基础模板
│   ├── index.html           # 主页面
│   ├── articles.html        # 文章列表
│   ├── article_edit.html   # 文章编辑
│   ├── generate.html        # AI 生成页面
│   └── git.html             # Git 操作页面
├── static/
│   └── style.css            # 样式文件
├── config.yaml               # 配置文件
├── wechat.db                 # SQLite 数据库
└── requirements.txt          # 依赖
```

---

## 3. 功能设计

### 3.1 Web 界面

#### 页面结构
- **首页**: 仪表盘，显示最近发布文章、发布状态
- **文章管理**: 列表展示、新增、编辑、删除
- **发布控制**: 选择文章 → 发布到微信（草稿/直接发布）
- **Git 操作**: 查看状态、手动提交、手动 push
- **AI 生成**: 输入关键词 → 生成 Markdown

#### UI 风格
- 简洁的 Tailwind CSS
- 移动端适配
- 深色/浅色主题切换

### 3.2 数据库设计

#### articles 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| title | TEXT | 标题 |
| author | TEXT | 作者 |
| category | TEXT | 分类 |
| summary | TEXT | 摘要 |
| content | TEXT | 正文 (Markdown) |
| cover_image | TEXT | 封面图 URL |
| source_file | TEXT | 源文件名 |
| status | TEXT | 状态: draft/published |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### publish_logs 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| article_id | INTEGER | 文章 ID |
| mode | TEXT | 发布模式: draft/publish |
| wechat_media_id | TEXT | 微信素材 ID |
| published_at | DATETIME | 发布时间 |
| result | TEXT | 发布结果 |

#### config 表
| 字段 | 类型 | 说明 |
|------|------|------|
| key | TEXT | 配置键 |
| value | TEXT | 配置值 |

### 3.3 API 设计

#### 文章 API
- `GET /api/articles` - 获取文章列表
- `GET /api/articles/<id>` - 获取单篇文章
- `POST /api/articles` - 创建文章
- `PUT /api/articles/<id>` - 更新文章
- `DELETE /api/articles/<id>` - 删除文章

#### 发布 API
- `POST /api/publish` - 发布文章到微信
- `GET /api/publish/logs` - 获取发布日志

#### Git 操作 API
- `GET /api/git/status` - 获取 Git 状态
- `POST /api/git/commit` - 执行 git add + commit
- `POST /api/git/push` - 执行 git push
- `GET /api/git/log` - 获取提交历史

#### AI 生成 API
- `POST /api/ai/generate` - 生成文章
- `GET /api/ai/models` - 获取可用模型列表

#### Webhook API
- `POST /api/webhook/github` - GitHub Webhook 接收

#### 定时任务 API
- `GET /api/scheduler/status` - 获取定时任务状态
- `POST /api/scheduler/enable` - 启用定时任务
- `POST /api/scheduler/disable` - 禁用定时任务

### 3.4 GitHub Webhook 设计

#### 支持的事件
- `push` - 代码推送
- `pull_request` - PR 创建/更新

#### 处理流程
1. 接收 GitHub Webhook 请求
2. 验证签名（可选）
3. 解析事件类型
4. 根据配置执行相应操作：
   - 检查 articles/ 目录变更
   - 可选：自动发布新文章

### 3.5 AI 生成设计

#### 支持的模型
- GLM (智谱)
- Minimax
- Qwen (通义千问)

#### 生成流程
1. 用户输入关键词
2. 选择目标模型
3. 生成文章大纲 → 用户确认
4. 生成正文（适配公众号格式）
5. 保存到 articles/ 目录
6. 可选：直接发布

#### 公众号格式适配
- 标题限制 64 字符
- 作者限制 8 字符
- 内容转 HTML（微信支持）
- 代码块处理
- 图片处理

### 3.6 定时任务设计

#### 模式 A: Cron 模式
- 每天定时检查 articles/ 目录
- 新文章自动发布（可配置）

#### 模式 B: 文章驱动
- 新文章添加后 N 分钟自动发布
- 可配置延迟时间

#### 配置项
```yaml
schedule:
  enabled: true
  mode: cron  # cron | article-driven
  cron: "0 9 * * *"  # 每天 9 点
  delay_minutes: 30  # 文章驱动模式延迟
  auto_publish: false
```

---

## 4. 安全性设计

### 4.1 本地使用
- 无需认证（设计为本地工具）
- 建议配合防火墙使用

### 4.2 Webhook 签名
- 支持 GitHub Webhook 签名验证
- 可配置开启/关闭

### 4.3 API 限流
- 防止 API 滥用

---

## 5. 依赖设计

### Python 依赖
```txt
flask>=2.3.0
flask-cors>=4.0.0
sqlalchemy>=2.0.0
requests>=2.28.0
python-frontmatter>=1.0.0
pyyaml>=6.0
apscheduler>=8.0.0
```

---

## 6. 实施顺序

1. **基础设施**: Flask + SQLite + 数据模型
2. **核心功能**: 文章 CRUD + 发布功能
3. **Git 操作**: 状态/提交/push
4. **Web 界面**: 基础页面搭建
5. **AI 生成**: AI 写作模块
6. **Webhook**: GitHub Webhook
7. **定时任务**: Cron + 文章驱动
8. **优化**: UI 优化、功能完善
