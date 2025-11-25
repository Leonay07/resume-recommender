# 00_Development_Sequence.md

## 🧭 开发执行顺序与依赖说明

本文件定义整个简历推荐系统项目的开发顺序与依赖关系，确保所有模块在正确的阶段完成。

---

## 📦 一、总体执行顺序

```
01. 项目初始化（环境与结构）
      ↓
02. 前端结构设计
      ↓
03. 后端框架与接口骨架
      ↓
07. 后端抓取 Job 数据 + 传给 NLP 模型
      ↓
05. 模型接口定义与集成
      ↓
04. 前后端联调（fetch 测试）
      ↓
06. 部署 Hugging Face
```

---

## 🧱 二、依赖逻辑说明

| 步骤 | 依赖来源 | 原因 |
|------|-----------|------|
| ✅ 01_project_initialization.md | 无 | 初始化环境与目录结构 |
| ✅ 02_frontend_layout_structure.md | 依赖 01 | 前端设计需运行环境支持 |
| ✅ 03_backend_api_skeleton.md | 依赖 01 | 后端接口需在环境配置后创建 |
| 🆕 07_backend_to_nlp_integration.md | 依赖 03 | 需先有后端接口以调用模型 |
| ✅ 05_model_interface_stub.md | 依赖 07 | 模型接口需基于后端传入数据 |
| ✅ 04_frontend_backend_integration.md | 依赖 03、05 | 前后端对接需接口与模型已实现 |
| ✅ 06_docker_deployment_guide.md | 依赖全部模块 | 部署需系统完整运行 |

---

## ⚙️ 三、详细顺序与责任划分

| 顺序 | 模块 | 描述 | 负责人 |
|------|------|------|------|
| 1️⃣ | 01_project_initialization.md | 初始化项目、安装依赖、创建结构 | ✅ Yuang Li |
| 2️⃣ | 02_frontend_layout_structure.md | 前端页面布局与导航设计 | ✅ Yuang Li |
| 3️⃣ | 03_backend_api_skeleton.md | 定义 FastAPI 路由与基础逻辑 | ✅ Yuang Li |
| 4️⃣ | 07_backend_to_nlp_integration.md | 抓取 Job API、传给 NLP 模型 | ✅ Yuang Li |
| 5️⃣ | 05_model_interface_stub.md | 定义模型接口函数（留给 NLP 团队实现） | ✅ Yuang Li & ⚙️ NLP 团队 |
| 6️⃣ | 04_frontend_backend_integration.md | 联通前后端，测试数据流通 | ✅ Yuang Li |
| 7️⃣ | 06_docker_deployment_guide.md | 部署到 Hugging Face Spaces | ✅ Yuang Li |

---

## 🧩 四、关键依赖点总结

- `07_backend_to_nlp_integration.md` 是 **桥梁模块**，承上启下：  
  - 上承：后端 API 骨架（`03_backend_api_skeleton.md`）  
  - 下接：NLP 模型集成（`05_model_interface_stub.md`）  
  - 确保 job 数据能被模型使用，打通 resume → job → score 流程。

- `05_model_interface_stub.md` 必须在 `07` 完成后更新接口定义，确保模型端接收 `job_list` 格式一致。

---

## ✅ 五、最终顺序确认

| 阶段 | 模块 | 目标 |
|------|------|------|
| 初始化阶段 | 01 | 搭建基础工程 |
| 前端开发阶段 | 02 | 完成界面结构与交互逻辑 |
| 后端开发阶段 | 03 | 构建 API 框架 |
| 数据集成阶段 | 07 | 抓取 Job 数据并传入 NLP 模型 |
| 模型集成阶段 | 05 | 对接 NLP 模块 |
| 联调阶段 | 04 | 测试系统数据流 |
| 部署阶段 | 06 | 上线 Hugging Face Spaces |
