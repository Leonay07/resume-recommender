## 开发通用规范

### 一、命名规则
- 组件文件名使用 **PascalCase**：例如 `JobCard.tsx`
- 函数与变量命名使用 **camelCase**
- 路由路径使用 **小写中划线**：如 `/job-feed`
- 接口路径使用 **动词开头**：如 `/get-jobs`, `/match`

### 二、代码规范
- 所有前端组件必须为函数式组件。
- 后端接口均返回 JSON，包含 `status` 与 `data` 字段。
- 所有异步请求均使用 `async/await`。
- 禁止使用 any 类型，TypeScript 需定义接口类型。

### 三、文件组织
| 目录 | 内容 |
|------|------|
| `/src/pages` | 页面组件 |
| `/src/components` | 可复用 UI 组件 |
| `/src/types.ts` | 类型定义 |
| `/backend/app.py` | FastAPI 主程序 |
| `/backend/nlp_model_stub.py` | NLP 模型接口占位 |

### 四、注释规范
- 关键逻辑必须附中文注释。  
- 每个接口定义前加说明注释，描述输入输出字段。  
- 模型文件须在函数体内注明“待替换逻辑”。

### 五、协作要求
- 提交代码需保证无 ESLint 报错。
- 文档内容更新需同步至 `/docs` 目录。
- 所有文件命名统一使用英文。
