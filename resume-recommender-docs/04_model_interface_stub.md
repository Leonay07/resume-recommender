## 模块 05：模型接口预留

### 目标
为 NLP 模型预留接口结构，使队友能直接在其中实现匹配逻辑。

### 结构
```
backend/
└── nlp_model_stub.py
```

### 函数定义
```python
def recommend_jobs(resume_text, job_list, title, location, experience):
    # TODO: 模型逻辑实现
    # 返回推荐岗位列表
    # 参数 job_list: 后端爬取的岗位数据（列表，每个元素为一个岗位字典）
    return [
        {"title": "Data Analyst", "company": "Google", "score": 0.87},
        {"title": "ML Engineer", "company": "Meta", "score": 0.81}
    ]
```

### app.py 调用逻辑
在 `/match` 接口中：
1. 解析上传的简历文本与筛选条件。
2. 从 JSearch API 获取岗位数据（job_list）；
3. 调用 `recommend_jobs()` 获取结果。
4. 将结果返回前端。

### 预留字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `resume_text` | string | 简历内容 |
| `title` | string | 用户填写的职位意向 |
| `location` | string | 用户选择的地区 |
| `experience` | string | 工作经验 |

### 测试要点
| 测试目标 | 验证方式 |
|-----------|-----------|
| 函数可被 app 调用 | 模拟 POST 请求调用 `/match` |
| 返回结构符合前端预期 | 返回数组含 title/company/score |
| 占位逻辑稳定 | 模型未实现时接口仍可运行 |
