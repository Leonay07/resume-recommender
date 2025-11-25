## 接口定义与字段约定

---

### 1️⃣ /jobs/random
**方法：** GET  
**功能：** 返回随机岗位列表（供前端展示）  

**返回示例：**
```json
[
  {
    "title": "Data Scientist",
    "company": "OpenAI",
    "location": "Remote",
    "description": "Analyze large datasets to develop data-driven insights.",
    "score": 0.91,
    "apply_link": "https://www.openai.com/careers/data-scientist"
  }
]
```

---

### 2️⃣ /jobs/search
**方法：** GET  
**功能：** 根据关键词搜索岗位  

**请求参数：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `title` | string | 搜索关键字或岗位名称 |
| `location` | string | 筛选地区 |

**返回示例：**
```json
[
  {
    "title": "ML Engineer",
    "company": "Meta",
    "location": "NY",
    "description": "Work on machine learning infrastructure and production models.",
    "score": 0.88,
    "apply_link": "https://www.metacareers.com/ml-engineer"
  }
]
```

---

### 3️⃣ /match
**方法：** POST  
**功能：** 上传 PDF 简历并返回匹配岗位推荐结果  

**请求体（multipart/form-data）：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `file` | file | 用户上传的 PDF 简历文件 |
| `title` | string | 用户输入的目标职位 |
| `location` | string | 用户选择的地区 |
| experience | string | 用户在前端下拉菜单中选择的经验档次，可选值："0"（无经验）、"1-3"、"3-5"、"5+"，若未选择则默认 "0"（初级/学生）。 |

> ⚙️ 说明：  
> 后端接收该请求后，将四个字段传入模型函数  
> `recommend_jobs(file, title, location, experience)`。  
> 模型需自行解析 PDF 文件内容（由 NLP 组负责），从中提取文本用于岗位匹配。

---

**返回示例：**
```json
[
  {
    "title": "Machine Learning Engineer",
    "company": "Meta",
    "location": "Remote",
    "description": "Develop and deploy ML systems for recommendation ranking.",
    "score": 0.87,
    "apply_link": "https://www.linkedin.com/jobs/view/12345"
  },
  {
    "title": "Data Scientist",
    "company": "Google",
    "location": "NY",
    "description": "Build large-scale data pipelines and predictive models.",
    "score": 0.82,
    "apply_link": "https://careers.google.com/jobs/view/67890"
  }
]
```

---

**错误响应示例：**
```json
{
  "status": "error",
  "message": "Invalid file format or model processing error"
}
```

---

### 📘 字段规范总结

| 类别 | 字段 | 类型 | 说明 |
|------|------|------|------|
| 输入 | `file` | file | PDF 简历文件（二进制上传） |
| 输入 | `title` | string | 用户目标职位 |
| 输入 | `location` | string | 用户目标地区 |
| 输入 | `experience` | string | 用户经验年限 |
| 输出 | `title` | string | 推荐岗位标题 |
| 输出 | `company` | string | 公司名称 |
| 输出 | `location` | string | 岗位地区 |
| 输出 | `description` | string | 岗位简介 |
| 输出 | `score` | float | 匹配度（0–1） |
| 输出 | `apply_link` | string | 申请链接，可为空字符串 |

---

### 📌 统一约束说明

- 所有字段名与大小写必须严格一致；  
- 返回列表长度 ≤ 5；  
- `score` 值范围为 0.0–1.0，按降序排列；  
- 异常时返回空数组 `[]`；  
- 模型（NLP 组）负责简历 PDF 解析和匹配逻辑；  
- 后端仅负责文件传输与结果转发，不做 NLP 处理。


---

# ⚙️ 更新说明（Final Version）

本版本在保持原有结构的基础上，新增了未来兼容性和可扩展字段说明。

---

## ✅ /match 接口返回结果更新

为支持 NLP 模型后续输出匹配解释信息，接口返回结构中预留以下两个可选字段：

```json
[
  {
    "title": "Machine Learning Engineer",
    "company": "Meta",
    "location": "Remote",
    "description": "Develop and deploy ML systems for recommendation ranking.",
    "score": 0.87,
    "summary": "Your Python and AWS experience strongly match this job.",
    "evidence_image": "https://huggingface.co/spaces/team/output/sample123.png",
    "apply_link": "https://www.linkedin.com/jobs/view/12345"
  }
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `summary` | string | 模型生成的匹配摘要说明，可为空 |
| `evidence_image` | string (URL/base64) | 模型生成的图像解释，可为空 |
| `apply_link` | string | 岗位申请链接 |

> 💡 若模型暂未提供 `summary` 或 `evidence_image`，后端将以 `null` 或空字符串返回。

---

## ✅ 接口兼容性声明

> **兼容性设计：**
> - 模型返回的额外字段不会影响接口正常运行；  
> - 后端采用字段自适应机制，自动保留未知字段；  
> - 前端仅在字段存在时才渲染（使用条件判断）。  

该设计确保系统能在 NLP 模型迭代时保持前后端解耦，增强可维护性与长期稳定性。

---

## ✅ 返回数量规范更新

> - 返回列表长度 ≤ 10（按匹配分数降序排列）  
> - 若模型返回不足 10 条，前端应正常显示全部结果。

---

📘 本版本文件命名为 **api_contracts_final.md**，可直接作为系统接口规范最终交付版本使用。
