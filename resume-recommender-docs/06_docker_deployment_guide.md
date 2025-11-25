## 模块 06：部署规范（Docker + Hugging Face Spaces）

### 目标
将前端与后端通过 Docker 打包成统一容器，在 Hugging Face Spaces 上部署。

### 结构
```
resume-recommender/
│
├── frontend/
├── backend/
└── Dockerfile
```

### Dockerfile 内容说明
| 部分 | 说明 |
|------|------|
| 第一阶段 | 使用 Node 镜像构建前端，生成 dist 文件夹 |
| 第二阶段 | 使用 Python 镜像运行 FastAPI，并复制 dist 到静态目录 |
| 暴露端口 | 7860（Hugging Face 默认端口） |
| 启动命令 | `uvicorn backend.app:app --host 0.0.0.0 --port 7860` |

### 部署步骤
1. 上传整个项目至 Hugging Face Space（选择 SDK: Docker）。
2. 确认 `Dockerfile` 位于根目录。
3. 构建自动完成后访问 Space 链接。

### 测试要点
| 测试目标 | 验证方式 |
|-----------|-----------|
| 构建无报错 | Hugging Face 显示 “Running” 状态 |
| 页面能访问 | 访问 Space URL 显示前端界面 |
| 接口可响应 | 上传简历后接口返回推荐结果 |
| 性能稳定 | 页面加载与接口响应时间正常 |
