# 部署指南

## 环境要求

- Python 3.8+
- pip 包管理器
- Google Gemini API 密钥

## 本地开发部署

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd poetry
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制环境变量示例文件：
```bash
cp env_example.txt .env
```

编辑 `.env` 文件，填入您的配置：
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///poetry.db
GEMINI_API_KEY=your-gemini-api-key-here
```

### 5. 初始化数据库

```bash
python main.py
```

### 6. 运行应用

```bash
python main.py
```

访问 http://localhost:5000

## 生产环境部署

### 使用 Gunicorn (推荐)

1. 安装 Gunicorn：
```bash
pip install gunicorn
```

2. 创建 Gunicorn 配置文件 `gunicorn.conf.py`：
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

3. 启动服务：
```bash
gunicorn -c gunicorn.conf.py main:app
```

### 使用 Docker

1. 创建 `Dockerfile`：
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]
```

2. 创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  poetry-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./static/images:/app/static/images
      - ./poetry.db:/app/poetry.db
    restart: unless-stopped
```

3. 启动服务：
```bash
docker-compose up -d
```

### 使用 Nginx 反向代理

1. 安装 Nginx：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

2. 创建 Nginx 配置文件 `/etc/nginx/sites-available/poetry`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/poetry/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

3. 启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/poetry /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 数据库配置

### SQLite (默认)

适合小型应用，无需额外配置。

### PostgreSQL

1. 安装 PostgreSQL：
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
```

2. 创建数据库：
```sql
CREATE DATABASE poetry_db;
CREATE USER poetry_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE poetry_db TO poetry_user;
```

3. 更新环境变量：
```env
DATABASE_URL=postgresql://poetry_user:your_password@localhost/poetry_db
```

4. 安装 PostgreSQL 驱动：
```bash
pip install psycopg2-binary
```

### MySQL

1. 安装 MySQL：
```bash
# Ubuntu/Debian
sudo apt install mysql-server

# CentOS/RHEL
sudo yum install mysql-server
```

2. 创建数据库：
```sql
CREATE DATABASE poetry_db;
CREATE USER 'poetry_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON poetry_db.* TO 'poetry_user'@'localhost';
FLUSH PRIVILEGES;
```

3. 更新环境变量：
```env
DATABASE_URL=mysql://poetry_user:your_password@localhost/poetry_db
```

4. 安装 MySQL 驱动：
```bash
pip install PyMySQL
```

## 安全配置

### 1. 设置强密钥

```python
import secrets
print(secrets.token_hex(32))
```

### 2. 配置 HTTPS

使用 Let's Encrypt 免费 SSL 证书：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. 防火墙配置

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 监控和日志

### 1. 应用日志

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/poetry.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Poetry app startup')
```

### 2. 系统监控

使用 systemd 管理服务：

创建 `/etc/systemd/system/poetry.service`：
```ini
[Unit]
Description=Poetry App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/poetry
Environment=PATH=/path/to/poetry/venv/bin
ExecStart=/path/to/poetry/venv/bin/gunicorn -c gunicorn.conf.py main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable poetry
sudo systemctl start poetry
```

## 备份策略

### 1. 数据库备份

```bash
# SQLite
cp poetry.db poetry_backup_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL
pg_dump poetry_db > poetry_backup_$(date +%Y%m%d_%H%M%S).sql

# MySQL
mysqldump poetry_db > poetry_backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. 图片备份

```bash
tar -czf images_backup_$(date +%Y%m%d_%H%M%S).tar.gz static/images/
```

### 3. 自动备份脚本

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/poetry"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
cp poetry.db $BACKUP_DIR/poetry_$DATE.db

# 备份图片
tar -czf $BACKUP_DIR/images_$DATE.tar.gz static/images/

# 清理旧备份（保留30天）
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

添加到 crontab：
```bash
# 每天凌晨2点备份
0 2 * * * /path/to/backup.sh
```
