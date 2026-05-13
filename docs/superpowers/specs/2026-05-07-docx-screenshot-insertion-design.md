---
name: docx-screenshot-insertion
description: Insert system page screenshots and descriptions into graduation thesis Chapter 5.3
type: project
---

# System Page Screenshots Insertion into Thesis

## Task

Insert screenshots of all 8 system pages with functional descriptions into the graduation thesis (初稿(1).docx), specifically in Chapter 5.3 (前端界面实现).

## Pages to Screenshot

1. HomePage - 系统首页
2. LoginPage - 登录页面
3. DrugRecommendation - 用药推荐页面
4. PatientRecords - 患者管理页面
5. PrivacyConfig - 隠私配置页面
6. PrivacyVisualization - 隐私可视化页面
7. AdminDashboard - 管理员仪表盘
8. ForbiddenPage - 403禁止访问页面

## Implementation Steps

### Step 1: Start Services & Take Screenshots
- Start frontend (5173), backend (8080), model service (8001)
- Use Playwright to navigate each page and screenshot
- Pages requiring login: DrugRecommendation, PatientRecords, PrivacyConfig, PrivacyVisualization, AdminDashboard
- Login first as admin/admin123, then navigate to each page

### Step 2: Write Functional Descriptions
- Chinese descriptions matching thesis style
- Format: （N）页面名称：功能描述。界面如图5-N所示。

### Step 3: Insert into Docx with python-docx
- Insert after paragraph [207] in 5.3 section
- Each group: description paragraph + centered image (width ~14cm)
- Use Normal style consistent with original document

## Image Settings
- Width: ~14cm (A4 page width ~16cm, leave margins)
- Centered alignment
- Numbered as 图5-1 through 图5-8

**Why:** Thesis Chapter 5.3 currently has only brief text without visual evidence of system implementation. Adding screenshots provides concrete evidence of the system's functionality.

**How to apply:** Execute via Playwright screenshots + python-docx insertion into the original docx file.