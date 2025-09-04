# 诗歌创作平台

一个集成了AI图像生成功能的诗歌创作和管理平台。用户可以创作诗词，系统会自动根据诗词内容生成配图，并提供图片下载功能。

## 功能特性

- ✍️ **诗词创作与编辑**: 支持创建、编辑、删除诗词
- 🎨 **AI自动配图**: 根据诗词内容自动生成配图
- 📱 **响应式设计**: 美观的现代化界面，支持移动端
- 💾 **图片下载**: 支持下载生成的配图
- 🗄️ **数据持久化**: 使用SQLite数据库存储诗词和图片信息

## 技术栈

- **后端**: Flask + SQLAlchemy
- **前端**: Bootstrap 5 + Font Awesome
- **AI服务**: Google Gemini API
- **数据库**: SQLite
- **图片处理**: Python内置库

## 安装和运行

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd poetry
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `env_example.txt` 为 `.env` 并填入您的配置：
```bash
cp env_example.txt .env
```

编辑 `.env` 文件，填入您的Google Gemini API密钥：
```
GEMINI_API_KEY=your-gemini-api-key-here
```

### 4. 运行应用
```bash
python main.py
```

访问 http://localhost:5000 即可使用应用。

## 使用说明

### 创作诗词
1. 点击"创作诗词"按钮
2. 填写诗词标题、作者和内容
3. 点击"保存并生成配图"
4. 系统会自动根据诗词内容生成配图

### 查看诗词
- 首页显示所有诗词的缩略图
- 点击"查看"按钮可以查看完整内容
- 图片居中显示，诗词内容在右侧

### 编辑诗词
- 点击"编辑"按钮可以修改诗词内容
- 修改后系统会重新生成配图

### 下载图片
- 在诗词详情页面点击"下载图片"按钮
- 图片会以诗词标题命名下载

## 项目结构

```
poetry/
├── main.py                    # 主启动文件
├── config.py                  # 配置文件
├── requirements.txt           # 依赖包列表
├── env_example.txt           # 环境变量示例
├── README.md                 # 项目说明
├── poetry_app/               # 应用包
│   ├── __init__.py          # 应用工厂
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   └── poetry.py        # 诗词模型
│   ├── routes/              # 路由模块
│   │   ├── __init__.py
│   │   ├── main.py          # 主页面路由
│   │   ├── poetry.py        # 诗词相关路由
│   │   └── api.py           # API接口路由
│   ├── services/            # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── ai_service.py    # AI图像生成服务
│   │   └── poetry_service.py # 诗词业务服务
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── helpers.py       # 辅助函数
├── templates/               # HTML模板
│   ├── base.html           # 基础模板
│   ├── index.html          # 首页
│   ├── about.html          # 关于页面
│   └── poetry/             # 诗词相关模板
│       ├── create.html     # 创作页面
│       ├── view.html       # 查看页面
│       └── edit.html       # 编辑页面
├── static/                 # 静态文件
│   ├── css/               # 样式文件
│   │   └── style.css      # 自定义样式
│   ├── js/                # JavaScript文件
│   │   └── main.js        # 主要脚本
│   └── images/            # 生成的图片存储目录
├── tests/                  # 测试文件
│   ├── __init__.py
│   └── test_models.py     # 模型测试
└── docs/                   # 文档
    ├── API.md             # API接口文档
    └── DEPLOYMENT.md      # 部署指南
```

## API接口

### Web页面路由
- `GET /` - 首页，显示所有诗词
- `GET /poetry/create` - 创作诗词页面
- `POST /poetry/create` - 创建新诗词
- `GET /poetry/<id>` - 查看指定诗词
- `GET /poetry/<id>/edit` - 编辑诗词页面
- `POST /poetry/<id>/edit` - 更新诗词
- `POST /poetry/<id>/delete` - 删除诗词
- `GET /poetry/<id>/download` - 下载图片
- `GET /about` - 关于页面

### REST API接口
- `GET /api/poems` - 获取所有诗词的JSON数据
- `GET /api/poems/<id>` - 获取指定诗词的JSON数据
- `GET /api/poems/search?q=<keyword>` - 搜索诗词
- `GET /api/poems/recent?limit=<num>` - 获取最近的诗词
- `GET /api/stats` - 获取统计信息

## 注意事项

1. 需要有效的Google Gemini API密钥才能使用AI图像生成功能
2. 生成的图片会保存在 `static/images/` 目录下
3. 数据库文件 `poetry.db` 会在首次运行时自动创建
4. 建议定期备份数据库和图片文件

## 许可证

MIT License