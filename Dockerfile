FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 Node.js
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制前端代码
COPY frontend/package.json frontend/package-lock.json* ./frontend/

# 安装前端依赖
WORKDIR /app/frontend
RUN npm install

# 复制前端源代码并构建
COPY frontend/ ./
RUN npm run build

# 返回主目录
WORKDIR /app

# 复制后端代码
COPY app.py .
COPY config.yaml .
COPY api/ ./api/
COPY models.py .
COPY database.py .
COPY scheduler.py .
COPY git_helper.py .
COPY ai_writer.py .
COPY wechat_publisher.py .
COPY templates/ ./templates/
COPY static/ ./static/

# 创建文章目录
RUN mkdir -p articles

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]
