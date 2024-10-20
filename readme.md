---

## **BookBoomer**

---

### 效果展示
![image](https://github.com/user-attachments/assets/f766386d-4c45-46e6-9335-6444ed709c7f)

其中的md文件例：

![image](https://github.com/user-attachments/assets/8d43ee9e-8af5-4708-9aa1-5972c6eba5b3)

用户在进行学习的时候，可以在复习点中添加自己对于这个知识点的理解，也可以添加用于快速复习的教程

包含的元数据：

![image](https://github.com/user-attachments/assets/cd83964f-aeb2-48aa-851b-3e0399d09579)

元数据可以用于在黑曜石中管理相关的文件。

在OB里配置一下，结合foldernote和模板就可以达到类似这种效果:

![image](https://github.com/user-attachments/assets/60c24091-0771-4bf9-b3c7-da45cb9c40c7)

### 1. 项目简介

**BookBoomer** 是一个辅助工具，旨在帮助用户从 **PDF 书籍**（尤其是教材）中高效提取知识点，并将其自动转换为 **Markdown 文件**，按目录结构进行存储和分类。该工具通过目录解析、自动生成 Markdown 文件、递归文件夹管理等功能，为用户构建一套便于学习和整理的知识体系。

---

### 2. 使用场景

在面对一本书时，尤其是一本**教材**或**专业书籍**时，书中涉及的**新概念和复杂结构**，常常让用户感到压迫感和“学习恐惧”。这种恐惧会影响学习的心态，并降低学习效率。然而，通过 **BookBoomer**，用户可以**提前预习知识点**，在正式阅读之前快速熟悉其中的概念。这个过程不仅减轻了学习压力，还帮助用户对知识形成整体框架，从而增强学习信心。

此外，本项目支持生成的 Markdown 文件以 **黑曜石(Obsidian)** 为目标格式。由于黑曜石支持在 **PC 和移动端同步使用**，用户可以利用**零散时间**（如地铁、公交等）进行**碎片化学习**，逐步掌握知识点。  
这种提前预习和主动学习的模式，有助于用户在正式学习时更轻松地理解内容，减少心理负担，实现高效学习。

---

### 3. 灵感来源

**BookBoomer** 的设计灵感来自于：

1. **卢曼卡片系统（Zettelkasten）**：  
   卢曼通过构建卡片系统，将复杂的知识拆解为**原子化**的卡片，并通过链接实现知识之间的联系。这种模式极大地提升了知识管理和思考效率。

2. **原子笔记（Atomic Notes）**：  
   **每个知识点**被独立记录，便于后续复习和检索。这种笔记方法与黑曜石应用中的**双向链接**思想高度契合，有助于用户在学习过程中建立连贯的知识体系。

---

### 4. 项目结构

```bash
BookBoomer/
│
├── main.py                    # 主程序入口
├── config.yaml                # 配置文件
├── src/                       # 核心代码
│   ├── config_loader.py       # 加载配置文件
│   ├── pdf_parser.py          # 处理 PDF 文件
│   ├── model_interface.py     # 调用大语言模型接口
│   ├── folder_generator.py    # 基于目录生成文件夹
│   ├── content_splitter.py    # 处理章节并生成 Markdown 文件
│   ├── yaml_utils.py          # YAML 解析与验证工具
└── tmp_storage/               # 临时存储目录
    ├── toc.yml                # 生成的目录文件
    └── content/               # 生成的文件夹与 Markdown 文件
```

---

### 5. 安装与运行

#### 5.1 环境要求

- Python 3.8+
- `pip` 包管理器

#### 5.2 安装依赖

在项目根目录下运行以下命令：

```bash
pip install -r requirements.txt
```

#### 5.3 运行程序

在项目根目录下运行以下命令启动程序：

```bash
python main.py
```

---

### 6. 配置文件说明 (`config.yaml`)

```yaml
storage:
  base_dir: "./tmp_storage"   # 存储目录

model:
  name: "gpt-4o-mini"         # 使用的语言模型
  api_key: "your-openai-api-key"  # OpenAI API 密钥
  max_tokens: 3000
  temperature: 0.7

book:                                # 用户自定义内容
  pdf_file: "data/example_book.pdf"  # PDF 文件路径
  toc_start: 44                      # 目录起始页
  toc_end: 49                        # 目录结束页
  content_start: 50                  # 正文起始页
  content_end: 300                   # 正文结束页

retry:
  max_attempts: 3                    # 重试次数
```

---

### 7. 使用说明

1. **生成目录**：
   - 程序将从用户指定的页码范围内提取目录，并生成 `toc.yml` 文件。

2. **用户确认目录**：
   - 用户可选择使用生成的目录文件或上传自定义目录文件。

3. **生成文件夹结构**：
   - 基于目录生成文件夹，格式为：`1-章节名`，`1-1-子章节名`。

4. **生成 Markdown 文件**：
   - 程序将根据目录结构和章节内容生成 Markdown 文件，并存放在最底层的文件夹中。

---

### 8. 常见问题

- **问题：生成的目录文件格式不正确**
  - 解决方案：检查生成的 `toc.yml` 文件是否符合预期。如果不符合，编辑或上传自定义目录文件。

- **问题：模型接口调用失败**
  - 解决方案：检查 API 密钥是否正确，或尝试增加重试次数。

- **问题：文件夹重复创建**
  - 解决方案：确保 `content_splitter.py` 和 `folder_generator.py` 使用相同的路径。

---

### 9. 未来展望
#### 改进方向
1. 支持更多语言的目录解析和内容生成。
2. 加上页面信息，用户在ob中能直接跳转到对应页面
3. 章节总结内容
4. ~~基于章节形成文件夹~~
2. 联网搜索相关教程
3. 图形化页面
4. ~~多模态~~
5. 目录识别与导入（用户可以自己输入目录页的范围，以及正文开始的范围，然后根据章节分类去爬知识点）
6. 重复知识点的去重
7. 有的pdf自带目录信息，可以直接提取啊
7. （待定）包装为一个OB插件


目前存在的问题：
1. 重复知识点
2. 知识点颗粒度不够
3. md文档生成未分割
---

### 10. 贡献指南

欢迎任何形式的贡献！如果你想参与项目开发，请按以下步骤进行：

1. Fork 此项目到你的 GitHub 账户。
2. 创建一个新分支并进行开发：
   ```bash
   git checkout -b feature-branch
   ```
3. 提交更改并推送到你的分支：
   ```bash
   git add .
   git commit -m "添加新功能"
   git push origin feature-branch
   ```
4. 创建 Pull Request，开发者会尽快审查你的更改。
---
# 祝学习愉快！
