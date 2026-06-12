# Knowledge Agent

企业知识库 Agent 系统

## 项目简介

基于 FastAPI + LangChain + Chroma + DeepSeek 构建的企业知识库问答系统。

支持：

- 用户注册登录
- JWT身份认证
- 文档上传
- 文档解析
- 向量化存储
- RAG检索增强生成
- Agent工具调用

---

## 技术栈

### Backend

- FastAPI
- SQLAlchemy
- MySQL
- JWT

### AI

- LangChain
- DeepSeek API
- ChromaDB
- Embedding Model

### Deploy

- Docker
- Nginx

---

## 当前开发进度

### 用户系统

- [x] 用户注册
- [x] 用户登录
- [x] JWT认证
- [x] 获取当前用户

### 知识库（Document模块）

- [x] 文件上传（UploadFile + UUID存储）
- [x] 文件类型校验（后缀 + Content-Type）
- [x] 文件大小限制（20MB）
- [x] 文件元数据入库（MySQL + SQLAlchemy）
- [x] 用户级文件隔离（user_id绑定）
- [ ] PDF解析
- [ ] DOCX解析
- [ ] 向量化

### RAG

- [ ] 文档切分
- [ ] Embedding
- [ ] Chroma
- [ ] 检索增强

### Agent

- [ ] Tool Calling
- [ ] 多工具编排

---

## 项目结构

app/
│
├── core/              # 配置与依赖
├── database/          # 数据库连接
├── models/            # ORM模型
├── schemas/           # Pydantic模型
├── routers/           # 路由
│   ├── user.py
│   ├── document.py
│
├── utils/             # 工具类
│   ├── jwt.py
│   ├── security.py
│
├── uploads/           # 文件存储目录
│   └── documents/
│
└── main.py

---

## 开发日志

### Day1

- FastAPI项目初始化
- MySQL连接
- SQLAlchemy配置
- 用户模型设计

### Day2

- 用户注册
- bcrypt密码加密
- JWT登录认证
- 获取当前用户

### Day3

- 实现 Document 文件上传模块
- 支持文件上传接口（/document/upload）
- 文件UUID重命名存储
- 文件大小限制与安全校验
- Content-Type + 后缀双重校验
- 用户级数据绑定（JWT + current_user）
- 文件信息写入数据库（Document表）

### Day4（计划）

- Document列表接口（分页查询）
- 用户级数据隔离查询
- SQLAlchemy filter优化
- response_model标准化