# 微信公众号发布工具

一个基于 Flask + Vue3 的微信公众号文章管理和发布工具，支持 AI 生成文章、定时发布、Git 同步等功能。

## 功能特性

- 📝 文章管理 - 创建、编辑、删除 Markdown 文章
- 🤖 AI 生成 - 支持 GLM、Minimax、Qwen 等大模型生成文章
- 📅 定时发布 - 支持 Cron 表达式定时发布文章
- 🔄 Git 同步 - 自动提交推送文章到 Git 仓库
- 🏷️ 草稿模式 - 支持预览模式，确认后再发布
- 🌐 多语言界面 - 支持中文/English

## 本地部署

### 前置要求

- Python 3.8+
- Node.js 18+
- SQLite

### 1. 克隆项目

```bash
git clone <repository-url>
cd wechat-publisher
```

### 2. 配置

复制并编辑配置文件：

```bash
cp config.yaml config.yaml.bak
# 编辑 config.yaml，填入你的微信公众号和 AI API 密钥
```

关键配置项说明：

```yaml
wechat:
  appid: "your-appid"        # 微信公众号 AppID
  secret: "your-secret"      # 微信公众号 AppSecret

ai:
  default_model: glm         # 默认 AI 模型
  glm:
    api_key: "your-api-key"  # 智谱 API Key

articles_dir: "./articles"  # 文章存储目录

publish:
  draft_mode: true           # 草稿模式，发布到草稿箱
```

### 3. 启动后端

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

后端服务将在 http://localhost:5000 启动

### 4. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 5. 生产构建

```bash
cd frontend
npm run build
```

构建产物将输出到 `frontend/dist` 目录

## Docker 部署

### 1. 构建镜像

```bash
docker build -t wechat-publisher .
```

### 2. 运行容器

```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/articles:/app/articles \
  -v $(pwd)/wechat.db:/app/wechat.db \
  --name wechat-publisher \
  wechat-publisher
```

### 3. 使用 Docker Compose（推荐）

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  wechat-publisher:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./articles:/app/articles
      - ./wechat.db:/app/wechat.db
    environment:
      - PORT=5000
      - DEBUG=false
    restart: unless-stopped
```

启动服务：

```bash
docker-compose up -d
```

服务将在 http://localhost:5000 启动

### 注意事项

- 首次运行会自动创建 SQLite 数据库文件
- 文章文件存储在 `articles` 目录
- 配置修改后需要重启容器

## API 文档

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/articles` | GET | 获取文章列表 |
| `/api/articles` | POST | 创建新文章 |
| `/api/articles/<id>` | GET | 获取文章详情 |
| `/api/articles/<id>` | PUT | 更新文章 |
| `/api/articles/<id>` | DELETE | 删除文章 |
| `/api/publish` | POST | 发布文章到微信 |
| `/api/generate` | POST | AI 生成文章 |
| `/api/config` | GET/PUT | 配置管理 |

## 目录结构

```
wechat-publisher/
├── app.py                 # Flask 主应用
├── config.yaml            # 配置文件
├── requirements.txt       # Python 依赖
├── wechat.db             # SQLite 数据库
├── articles/             # Markdown 文章目录
├── api/                  # API 路由
│   ├── articles.py
│   ├── publish.py
│   ├── ai_gen.py
│   ├── git_ops.py
│   └── ...
├── frontend/             # Vue3 前端
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── templates/            # HTML 模板
└── static/              # 静态文件
```

## 许可证

MIT License
