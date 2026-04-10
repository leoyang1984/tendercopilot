# tendercopilot

> 建筑/工程咨询标书编写与查重 · Claude Code 插件

面向建筑设计、市政工程、全过程工程咨询从业者。将招标文件转化为技术扎实的投标方案，并对已有文档进行查重分析。

---

## 安装

在终端运行：

```bash
claude /plugin marketplace add leoyang1984/tendercopilot
claude /plugin install tendercopilot@tendercopilot
```

安装后，以下命令在 Claude Code 中全局可用。

---

## 命令列表

| 命令 | 作用 |
|------|------|
| `/tendercopilot:bid-write` | 全流程标书编写：需求解析 → 写作大纲 → 分章撰写 → Word 交付 |
| `/tendercopilot:check-plagiarism` | 检测指定文件夹内 Word 文档之间的文本相似度，生成查重报告 |

---

## 前置依赖

### `/tendercopilot:bid-write`

需要安装 [Pandoc](https://pandoc.org/installing.html)，用于将 Markdown 转换为 Word 文档：

```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc

# Windows
choco install pandoc
```

### `/tendercopilot:check-plagiarism`

需要 Python 3 及以下库：

```bash
pip install python-docx scikit-learn
```

---

## 使用方式

### 标书编写

在存放招标文件的项目目录下启动 Claude Code，输入：

```
/tendercopilot:bid-write
```

Claude 会引导你完成以下流程：

1. **初始化工作区** — 自动创建 `requirements/`、`cases/`、`output/` 目录
2. **读取招标文件** — 支持 `.docx`（自动转 Markdown）和 `.md`、`.txt`
3. **生成写作大纲** — 需求对标矩阵 + 核心策略，等待你确认
4. **分章迭代撰写** — 每轮 1–2 章，自动质检，等待你审阅
5. **导出 Word 文档** — 支持自定义 `reference.docx` 样式模板

**工作区结构：**

```
你的项目目录/
├── requirements/        ← 放招标文件（.docx / .txt）
├── cases/               ← 放参考案例
│   └── priority/        ← 重点参考案例（可选）
├── output/              ← 生成文件输出目录
└── reference.docx       ← Word 样式模板（可选）
```

### 文档查重

```
/tendercopilot:check-plagiarism
```

Claude 会询问目标文件夹路径，扫描其中所有 `.docx` 文件，输出查重报告。

**报告包含：**
- 高风险对（相似度 > 70%）：🚨 标出，附修改建议
- 中等风险对（40%–70%）：表格列出
- 整体原创度评估

---

## 许可证

本项目仅供**个人学习和教育用途**使用，**不允许商业使用**。

详见 [LICENSE](./LICENSE) 文件。如需商业授权，请通过 [GitHub](https://github.com/leoyang1984) 联系作者。
