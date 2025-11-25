## 模块 01：项目初始化

### 目标
建立项目的基础结构，包括前端（React + Vite）与后端（FastAPI）两部分，确保二者独立可运行。

### 项目结构
```
resume-recommender/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── venv/
│
└── README.md
```

### 主要任务
1. 创建前后端目录与基础文件。
2. 确保前端可本地运行（显示默认页面）。
3. 确保后端可本地运行（返回 JSON）。
4. 检查端口无冲突（前端默认 5173，后端 8000）。

### 需添加的文件
| 文件路径 | 内容 |
|-----------|------|
| `frontend/` | 使用 React + TypeScript 模板初始化项目 |
| `backend/app.py` | 创建 FastAPI 实例，返回 “Hello from backend” |
| `backend/requirements.txt` | 列出 fastapi、uvicorn |
| `README.md` | 记录开发环境信息与运行说明 |

### 预留部分
- `.env` 文件：后续联调时添加。
- `/jobs/random` 与 `/match` 接口：后续模块实现。

### 测试要点
| 测试目标 | 验证方式 |
|-----------|----------|
| 前端运行正常 | 启动前端后访问本地端口显示页面 |
| 后端运行正常 | 访问后端端口返回 JSON |
| 同时运行无冲突 | 前后端同时启动无报错 |
