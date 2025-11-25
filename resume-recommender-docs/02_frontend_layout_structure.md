## 模块 02：前端页面结构与组件设计

### 目标
建立前端页面层级与组件结构，使用假数据展示内容，完成整体 UI 雏形。

### 结构
```
frontend/
│
└── src/
    ├── pages/
    │   ├── LandingPage.tsx
    │   ├── JobFeedPage.tsx
    │   ├── SearchPage.tsx
    │   └── ResultPage.tsx
    ├── components/
    │   └── JobCard.tsx
    └── App.tsx
```

### 页面说明
| 页面 | 功能 |
|------|------|
| LandingPage | 系统欢迎页，介绍与开始按钮 |
| JobFeedPage | 展示随机岗位（后端 `/jobs/random`）的结果 |
| SearchPage | 上传简历与选择条件（地区、经验、title） |
| ResultPage | 显示 NLP 匹配结果 |
| JobCard | 职位展示组件，包含标题、公司、匹配分数等 |

### 字段设计
| 字段 | 类型 | 用途 |
|------|------|------|
| `title` | string | 岗位标题 |
| `company` | string | 公司名称 |
| `location` | string | 工作地点 |
| `score` | number | 匹配度分数 |
| `description` | string | 职位描述 |

### 预留内容
- 上传简历按钮功能：暂不实现，仅渲染。
- ResultPage 数据：使用假数据展示。

### 测试要点
| 测试目标 | 验证方式 |
|-----------|-----------|
| 页面能正确切换 | 检查路由是否跳转正确 |
| UI 正常渲染 | 所有组件显示无报错 |
| 假数据展示正常 | 页面能显示静态岗位数据 |
