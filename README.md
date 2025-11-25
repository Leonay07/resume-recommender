# Resume Recommender 开发说明

本项目包括 React/Vite 前端与 FastAPI 后端，并最终通过 Docker 部署到 Hugging Face Spaces。以下内容覆盖开发环境准备与容器化运行方式。

---

## 环境依赖
- Python 3.10+
- Node.js 18+（默认使用 npm）
- Docker 与 Docker Compose（可选，用于一键容器化）
- RapidAPI 的 JSearch Key：请在 `backend/.env` 中配置
  ```
  RAPID_API_KEY=xxxx
  RAPID_API_HOST=jsearch.p.rapidapi.com
  ```

---

## 一键安装开发依赖

首次拉取代码后，执行根目录下的脚本即可完成后端虚拟环境与前端依赖安装：

```bash
chmod +x setup_local.sh   # 仅首次需要
./setup_local.sh
```

- 后端会在 `backend/.venv` 中创建虚拟环境，并安装 `requirements.txt`
- 前端在 `frontend/` 目录执行 `npm install`

---

## 本地开发启动

准备完成后，开启两个终端：

1. **后端（FastAPI + mock NLP）**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn app:app --reload --port 8000
   ```
2. **前端（Vite 开发服务器）**
   ```bash
   cd frontend
   npm run dev
   ```

- 前端默认监听 `http://localhost:5173`，后端 `http://localhost:8000`
- `/match` 目前使用 `backend/nlp_model_stub.py` 中的固定返回，用于前端联调；未来可直接替换为真实模型实现

## 配置api key
- **RapidAPI Key 缺失**：无 Key 时 Job API 会调用失败，请确认 `backend/.env` 已经配置（请替换成自己的apikey）

网站： https://rapidapi.com  搜索：JSearch

---

## 常见问题
- **静态文件缺失**：本地开发模式需使用 Vite 开发服务器；若直接 `uvicorn` 并访问 `/`，请先运行 `npm run build` 并将 `frontend/dist` 内容复制到 `backend/static/`。
- **NLP 模块尚未接入**：`nlp_model_stub.py` 返回的是 mock 数据，确保前端能预览详情页。真实模型可直接覆盖该函数接口。
- **Docker**：当前阶段以本地开发模式为主，待功能稳定后再使用 `run_docker.sh` 进行容器化验证/提交即可。

---

如需更多背景与 API 约定，请参阅 `resume-recommender-docs/` 与 `resume-recommender-docs-v2/` 中的规范文档。
