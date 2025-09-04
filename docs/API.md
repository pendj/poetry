# API 接口文档

## 概述

诗歌创作平台提供RESTful API接口，支持诗词的增删改查操作。

## 基础信息

- 基础URL: `http://localhost:5000/api`
- 数据格式: JSON
- 字符编码: UTF-8

## 接口列表

### 1. 获取所有诗词

**请求**
```
GET /api/poems
```

**响应**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "title": "春晓",
            "content": "春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。",
            "author": "孟浩然",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "image_path": "image_001.jpg",
            "image_prompt": "根据诗词《春晓》生成"
        }
    ],
    "count": 1
}
```

### 2. 获取单个诗词

**请求**
```
GET /api/poems/{id}
```

**参数**
- `id`: 诗词ID

**响应**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "春晓",
        "content": "春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。",
        "author": "孟浩然",
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00",
        "image_path": "image_001.jpg",
        "image_prompt": "根据诗词《春晓》生成"
    }
}
```

### 3. 搜索诗词

**请求**
```
GET /api/poems/search?q={keyword}
```

**参数**
- `q`: 搜索关键词

**响应**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "title": "春晓",
            "content": "春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。",
            "author": "孟浩然",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "image_path": "image_001.jpg",
            "image_prompt": "根据诗词《春晓》生成"
        }
    ],
    "count": 1,
    "keyword": "春"
}
```

### 4. 获取最近诗词

**请求**
```
GET /api/poems/recent?limit={limit}
```

**参数**
- `limit`: 返回数量限制（可选，默认10）

**响应**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "title": "春晓",
            "content": "春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。",
            "author": "孟浩然",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "image_path": "image_001.jpg",
            "image_prompt": "根据诗词《春晓》生成"
        }
    ],
    "count": 1
}
```

### 5. 获取统计信息

**请求**
```
GET /api/stats
```

**响应**
```json
{
    "success": true,
    "data": {
        "total_poems": 10,
        "total_authors": 5,
        "poems_with_images": 8,
        "image_coverage": 80.0
    }
}
```

## 错误响应

当请求失败时，API会返回错误信息：

```json
{
    "success": false,
    "error": "错误描述信息"
}
```

## 状态码

- `200`: 请求成功
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误

## 使用示例

### Python示例

```python
import requests

# 获取所有诗词
response = requests.get('http://localhost:5000/api/poems')
poems = response.json()

# 搜索诗词
response = requests.get('http://localhost:5000/api/poems/search?q=春')
results = response.json()

# 获取统计信息
response = requests.get('http://localhost:5000/api/stats')
stats = response.json()
```

### JavaScript示例

```javascript
// 获取所有诗词
fetch('/api/poems')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('诗词列表:', data.data);
        }
    });

// 搜索诗词
fetch('/api/poems/search?q=春')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('搜索结果:', data.data);
        }
    });
```
