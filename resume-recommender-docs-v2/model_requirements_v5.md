# NLP 模型接口规范（v5 最终版）

本文件定义 NLP 模型的输入、输出及与后端对接的参数要求。

---

## 一、输入字段说明

模型将从后端收到以下输入字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `file` | File | 用户上传的简历文件（PDF 或 DOCX） |
| `job_list` | list(dict) | 由后端通过 Job API 抓取的岗位数据 |
| `title` | string | 用户输入的目标岗位标题 |
| `location` | string | 用户选择的州简称或城市 |
| `experience` | string | 用户填写的经验年限（若为空则默认为 Entry-Level） |

> 💡 NLP 模型无需自行抓取岗位数据；后端会调用 Job API 并将结果以 `job_list` 参数传入。

### 🔹 job_list 数据结构示例

```json
[
  {
    "title": "Data Scientist",
    "company": "Google",
    "location": "CA",
    "description": "Analyze and model large-scale datasets.",
    "apply_link": "https://careers.google.com/jobs/view/67890"
  }
]
```

---

## 二、函数定义与调用示例

模型需实现以下核心函数：

```python
def recommend_jobs(resume_text: str, job_list: list[dict], title: str, location: str, experience: str):
    '''
    参数：
        resume_text: 从上传文件中提取的简历文本
        job_list: 后端爬取的岗位列表
        title: 用户输入的目标岗位
        location: 用户选择的州简称或城市
        experience: 用户填写的经验年限
    返回：
        岗位推荐结果的列表
    '''
```

### ✅ 调用示例

```python
# 后端调用
results = recommend_jobs(
    resume_text="Extracted resume text here",
    job_list=[{...}, {...}, {...}],
    title="Data Scientist",
    location="CA",
    experience="2"
)
```

> 模型应基于 resume_text 与 job_list 计算匹配分数与解释结果。  
> 若 job_list 为空，则返回空数组 `[]`。

---

## 三、输出字段定义

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `title` | string | 岗位名称 |
| `company` | string | 公司名称 |
| `location` | string | 岗位所在地区（州简称） |
| `description` | string | 岗位描述 |
| `score` | float | 模型计算的匹配分数（0~1） |
| `summary` | string (可选) | 模型生成的匹配摘要，用于解释推荐理由 |
| `evidence_image` | string (URL/base64，可选) | 模型生成的可视化解释，如技能匹配图或关键词词云 |
| `apply_link` | string | 岗位申请链接，可为空 |

---

### 🧠 evidence_image 字段格式说明

模型可在返回结果中包含解释性图片，支持以下两种格式：

1️⃣ **Hugging Face 上传链接**（推荐）：  
   `"https://huggingface.co/spaces/team/output/sample.png"`

2️⃣ **Base64 字符串（含前缀）**：  
   `"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."`

> 若未生成图片，返回 `null`。  
> 前端会自动根据字段类型完成渲染。

---

## 四、返回结果示例

```json
[
  {
    "title": "Machine Learning Engineer",
    "company": "Meta",
    "location": "DC",
    "description": "Develop and deploy ML systems for recommendation ranking.",
    "score": 0.87,
    "summary": "Your Python and AWS experience strongly match this job.",
    "evidence_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "apply_link": "https://www.linkedin.com/jobs/view/12345"
  }
]
```

---

## 五、格式与数量规范

> - 返回岗位数量 ≤ 10（按匹配分数降序排列）；  
> - 若无匹配结果，返回空数组 `[]`；  
> - 每个岗位对象必须至少包含 `title`、`score`、`company` 字段。

---

## 六、接口扩展与兼容性说明

> - 模型可在输出结果中新增额外字段（如 `keywords`、`confidence`、`insight_graph` 等）；后端会自动保留这些字段；  
> - 若某字段缺失，后端会填充默认值以保持接口稳定；  
> - 前端仅在字段存在时才渲染对应内容（条件渲染）；  
> - 模型不应修改输入参数结构或字段名。

---

📘 本文件为 **model_requirements_v5.md**，为 NLP 团队交付规范的最终版本。
