# 模块 04：前后端集成（v3 最终版）

## 🎯 模块目标
实现前端与后端接口的完整交互，包括简历上传、岗位推荐、分页加载，以及首页的随机岗位展示。

---

## 一、集成目标概述
| 功能 | 接口 | 说明 |
|------|------|------|
| 上传简历并推荐 | `/match` | 发送简历 + 用户输入信息，获取前10条岗位推荐 |
| 分页加载更多 | `/match/more` | 通过 offset 获取后续推荐 |
| 首页随机展示 | `/jobs/random` | 首页加载时显示随机岗位 |
| 模型接口调用 | `/match` 内部调用 NLP 模型 | 后端封装，不在前端暴露 |

---

## 二、前端主要组件交互结构
```
frontend/
│
├── components/
│   ├── ResumeUpload.tsx   # 上传简历组件
│   ├── JobCard.tsx        # 岗位卡片组件
│   └── Feed.tsx           # 展示岗位列表
│
├── pages/
│   ├── index.tsx          # 首页（随机展示）
│   └── result.tsx         # 上传简历后的推荐结果页
│
└── api/
    └── apiClient.ts       # 封装后端接口调用
```

---

## 三、数据流说明
```
[前端 ResumeUpload.tsx]
    ↓ 上传 PDF + 用户参数
POST /match
    ↓
[后端 FastAPI]
    ↓ 调用 NLP 模型计算匹配度
返回 JSON 结果 → Feed.tsx 渲染岗位卡片

用户点击 “Load More”
GET /match/more → 分页加载更多推荐岗位
```

---

## 四、接口调用封装（apiClient.ts）

```typescript
const BASE_URL = "https://your-hf-space-url.hf.space";

// 上传简历并获取推荐
export async function getMatchedJobs(formData) {
  const response = await fetch(`${BASE_URL}/match`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  return data.results || [];
}

// 分页加载更多结果
export async function getMoreJobs(offset = 10, limit = 10) {
  const response = await fetch(`${BASE_URL}/match/more?offset=${offset}&limit=${limit}`);
  const data = await response.json();
  return data.results || [];
}
```

---

## 五、前端展示逻辑（Feed.tsx）

```tsx
import JobCard from "./JobCard";

export default function Feed({ jobs }) {
  return (
    <div className="feed-container grid grid-cols-1 md:grid-cols-2 gap-4">
      {jobs.map((job, index) => (
        <JobCard key={index} job={job} />
      ))}
    </div>
  );
}
```

---

## 六、上传组件逻辑（ResumeUpload.tsx）

```tsx
import { useState } from "react";
import { getMatchedJobs } from "../api/apiClient";

export default function ResumeUpload({ onResults }) {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [experience, setExperience] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);
    formData.append("location", location);
    formData.append("experience", experience);

    const results = await getMatchedJobs(formData);
    onResults(results);
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
      <input type="text" placeholder="职位标题" onChange={(e) => setTitle(e.target.value)} />
      <input type="text" placeholder="地点 (州简称)" onChange={(e) => setLocation(e.target.value)} />
      <select onChange={(e) => setExperience(e.target.value)}>
        <option value="0">Entry Level</option>
        <option value="1-3">1-3 Years</option>
        <option value="3-5">3-5 Years</option>
        <option value="5+">5+ Years</option>
      </select>
      <button type="submit">上传并匹配</button>
    </form>
  );
}
```

---

## 七、首页随机岗位展示（新增接口 `/jobs/random`）

### 功能说明
- 用户首次进入网站（未上传简历）时，
  前端会调用 `/jobs/random` 接口，展示随机10条岗位。
- 页面结构沿用 Feed 组件与 JobCard 渲染逻辑。
- 用户上传简历后，自动切换到个性化推荐结果。

### 前端实现参考

```typescript
// apiClient.ts
export async function getRandomJobs() {
  const response = await fetch(`${BASE_URL}/jobs/random`);
  const data = await response.json();
  return data.results || [];
}
```

```tsx
// index.tsx
import { useEffect, useState } from "react";
import { getRandomJobs } from "../api/apiClient";
import Feed from "../components/Feed";

export default function HomePage() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    async function fetchJobs() {
      const randomJobs = await getRandomJobs();
      setJobs(randomJobs);
    }
    fetchJobs();
  }, []);

  return (
    <div className="home-container">
      <h1 className="text-2xl font-bold mb-4">🎯 欢迎使用简历推荐系统</h1>
      <Feed jobs={jobs} />
    </div>
  );
}
```

### 预期结果
| 场景 | 行为 | 预期 |
|------|------|------|
| 首次进入首页 | 调用 `/jobs/random` | Feed 展示随机10条岗位 |
| 上传简历 | 调用 `/match` | Feed 替换为推荐岗位 |
| 点击 “Load More” | 调用 `/match/more` | Feed 追加分页结果 |

---

## 八、完成标准
- ✅ 首页加载自动显示10条岗位；  
- ✅ 上传简历后切换到推荐结果；  
- ✅ “Load More” 分页可用；  
- ✅ 接口调用与后端文档一致（03_backend_api_skeleton_v4）。  
