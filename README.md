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

### 知识库

- [ ] 文件上传
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

待补充

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