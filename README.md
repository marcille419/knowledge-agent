# Knowledge Agent

企业知识库 Agent 系统

## 项目简介

基于 FastAPI + LangChain + ChromaDB + DeepSeek 构建的企业知识库问答系统。

系统支持：

* 用户注册登录
* JWT身份认证
* 文档上传管理
* 文档解析
* 文档切分（Chunk）
* 向量化存储
* RAG检索增强生成
* Agent工具调用

---

## 技术栈

### Backend

* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
* JWT

### AI

* LangChain
* DeepSeek API
* ChromaDB
* Embedding Model

### Deploy

* Docker
* Nginx

---

## 当前开发进度

### 用户系统

* [x] 用户注册
* [x] 用户登录
* [x] JWT认证
* [x] 获取当前用户

### 文档管理

* [x] 文件上传
* [x] 文件列表
* [x] 文件删除
* [x] 用户数据隔离
* [x] 文件大小校验
* [x] 文件类型校验

### 知识库

* [ ] PDF解析
* [ ] DOCX解析
* [ ] TXT解析
* [ ] 文档切分
* [ ] Chunk存储

### RAG

* [ ] Embedding
* [ ] ChromaDB
* [ ] 检索增强生成

### Agent

* [ ] Tool Calling
* [ ] 多工具编排

---

## 已实现接口

### 用户模块

POST /user/register

POST /user/login

GET /user/info

### 文档模块

POST /document/upload

GET /document/list

DELETE /document/{document_id}

---
```
## 项目结构

app/

├── core/             # 配置与认证

├── database/         # 数据库连接

├── models/           # ORM模型

├── schemas/          # Pydantic模型

├── routers/          # API路由

├── uploads/          # 文件存储目录

└── main.py
```
---

## 开发日志

### Day1

* FastAPI项目初始化
* MySQL连接
* SQLAlchemy配置
* 用户模型设计

### Day2

* 用户注册
* bcrypt密码加密
* JWT登录认证
* 获取当前用户

### Day3

* 文档上传接口
* 文件大小校验
* 文件类型校验
* UUID文件存储
* 文档信息入库

### Day4

* 文档列表接口
* 分页查询
* 用户数据隔离
* 文档删除接口
* 数据库事务处理
* 文件与数据库同步删除
* 异常处理与日志记录
