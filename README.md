# Knowledge Agent

Knowledge Agent 是一个基于 FastAPI 的企业知识库问答后端。项目支持用户认证、文档上传、文档解析、文本切分、Embedding 向量化、ChromaDB 向量检索，并通过兼容 OpenAI SDK 的大模型接口生成知识库问答结果。

## 功能概览

- 用户注册、登录和 JWT Bearer 认证
- 文档上传、分页列表、删除和重新处理
- 支持解析 `.pdf`、`.docx`、`.txt`、`.md` 文件
- 使用 LangChain `RecursiveCharacterTextSplitter` 对文档内容切分
- 使用 HuggingFace Embedding 模型生成向量
- 使用 ChromaDB 持久化向量数据
- 按用户隔离文档和检索结果
- 基于检索结果构建上下文并调用 LLM 生成回答

## 技术栈

- Web 框架：FastAPI、Uvicorn
- 数据库：MySQL、SQLAlchemy、PyMySQL
- 数据校验：Pydantic、pydantic-settings
- 认证：HTTP Bearer、JWT、bcrypt
- 文档解析：PyMuPDF、python-docx、charset-normalizer
- 文本切分：LangChain Text Splitters
- Embedding：langchain-huggingface、sentence-transformers
- 向量数据库：ChromaDB
- LLM 调用：OpenAI Python SDK，默认指向 DeepSeek API

## 目录结构

```text
.
├── app
│   ├── core              # 配置、依赖、模型加载、向量库封装
│   ├── database          # SQLAlchemy 连接、Base、建表脚本
│   ├── models            # ORM 模型
│   ├── routers           # API 路由
│   ├── schemas           # Pydantic 响应和请求模型
│   ├── services          # 文档处理、切分、向量化、检索、问答服务
│   ├── utils             # JWT 和密码工具
│   └── main.py           # FastAPI 应用入口
├── data
│   └── chroma            # ChromaDB 数据目录
├── .env.example          # 环境变量示例
├── requirements.txt      # Python 依赖
└── test_jwt.py           # JWT 简单验证脚本
```

## 环境要求

- Python 3.11+ 推荐
- MySQL 8.x 推荐
- 可访问 HuggingFace 模型下载源
- 可访问兼容 OpenAI Chat Completions 的 LLM 服务

## 快速开始

### 1. 创建虚拟环境

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

Git Bash：

```bash
source .venv/Scripts/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，并按本地环境修改：

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/knowledge_agent
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=knowledge_chunks
LLM_API_KEY=your_deepseek_api_key_here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-v4-flash
```

说明：

- `DATABASE_URL` 必须指向已创建的 MySQL 数据库。
- `EMBEDDING_MODEL` 会在应用启动时加载，首次运行可能需要下载模型。
- `CHROMA_PERSIST_DIR` 是 ChromaDB 持久化目录。
- `LLM_BASE_URL` 和 `LLM_MODEL` 可替换为其他兼容 OpenAI SDK 的服务。

### 4. 初始化数据库表

项目当前没有集成 Alembic，使用 SQLAlchemy `create_all` 初始化表：

```bash
python -m app.database.init_db
```

### 5. 启动服务

```bash
uvicorn app.main:app --reload
```

启动后访问：

- API 根路径：`http://127.0.0.1:8000/`
- Swagger 文档：`http://127.0.0.1:8000/docs`
- ReDoc 文档：`http://127.0.0.1:8000/redoc`

## 认证方式

登录成功后会返回 `token`。访问需要登录的接口时，在请求头中携带：

```http
Authorization: Bearer <token>
```

## API 列表

### 用户模块

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| `POST` | `/user/register` | 注册用户 | 否 |
| `POST` | `/user/login` | 登录并获取 token | 否 |
| `GET` | `/user/profile` | 获取当前登录用户信息 | 是 |
| `GET` | `/user/info` | 测试接口，返回固定用户信息 | 否 |

注册请求示例：

```json
{
  "username": "admin",
  "password": "123456"
}
```

登录响应中的 `data.token` 用于后续认证。

### 文档模块

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| `POST` | `/document/upload` | 上传文档 | 是 |
| `GET` | `/document/list` | 分页查询当前用户文档 | 是 |
| `DELETE` | `/document/{document_id}` | 删除文档及其数据库记录 | 是 |
| `POST` | `/document/{document_id}/process` | 解析、切分、向量化并写入 ChromaDB | 是 |

上传限制：

- 最大文件大小：20 MB
- 支持扩展名：`.pdf`、`.docx`、`.txt`、`.md`
- 文件会保存到 `app/uploads/documents`

文档处理流程：

```text
上传文件
  -> 保存文档元数据到 MySQL
  -> 调用 /document/{document_id}/process
  -> 解析文件文本
  -> 切分 chunk
  -> 保存 chunk 到 MySQL
  -> 生成 embedding
  -> 写入 ChromaDB
```

### 问答模块

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| `GET` | `/chat/retrieve?query=...&top_k=5` | 检索相关文档片段 | 是 |
| `GET` | `/chat/ask?query=...&top_k=5&debug=false` | 基于知识库生成回答 | 是 |

`/chat/ask` 返回内容包含：

- `query`：用户问题
- `answer`：模型回答
- `sources`：引用的 chunk 信息，包含 `chunk_id`、`document_id`、`filename`、`chunk_index` 和内容预览
- `prompt`：当 `debug=true` 时返回最终提示词

## 数据模型

当前主要表：

- `users`：用户账号和密码哈希
- `documents`：文档元数据、文件路径、类型、大小和所属用户
- `document_chunks`：文档切分后的文本片段

向量数据存储在 ChromaDB 中，metadata 包含：

- `document_id`
- `chunk_id`
- `user_id`

## 当前状态

已实现：

- 用户注册、登录、JWT 校验
- 文档上传、列表、删除
- PDF、DOCX、TXT、Markdown 解析
- 文档切分和 chunk 入库
- Embedding 生成和 ChromaDB 写入
- 按用户过滤的向量检索
- 基于检索结果的 RAG 问答
- 问答结果返回来源文件名和 chunk 内容预览
- 文档删除后异步清理 ChromaDB 向量数据，并记录清理失败日志

## 开发提示

- 应用启动时会加载 Embedding 模型并初始化 ChromaDB，首次启动可能较慢。
- 处理文档前必须先完成上传，并使用登录 token 调用处理接口。
- 当前 `JWT SECRET_KEY` 写在 `app/utils/jwt.py` 中，不适合生产环境直接使用。
- 当前建表脚本只负责创建表，不负责结构迁移；模型变更后需要自行处理数据库结构同步。
- `data/chroma/` 属于本地向量数据库运行数据，不应提交到 Git。
