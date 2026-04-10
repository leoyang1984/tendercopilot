---
name: tendercopilot:check-plagiarism
description: 文档查重检测。当用户需要检测 Word 文档之间的文本重复率、比对投标文件相似度、或对某个文件夹下的 docx 文件进行查重分析时触发。
---

# 文档查重检测 (Check-Plagiarism)

对指定文件夹内的 Word 文档（.docx）进行文本相似度检测，基于 TF-IDF 余弦相似度算法，输出结构化查重报告。

**输入**：包含多个 `.docx` 文件的文件夹路径
**输出**：Markdown 格式的查重分析报告

---

## 执行流程

### 步骤 1：确认路径

1. 从用户指令中提取目标文件夹路径，记为 `{target_folder}`。
2. 若用户未提供路径，询问："请问您需要检查哪个文件夹下的文档？"

### 步骤 2：执行检测脚本

先定位脚本，再执行：

```bash
SCRIPT=$(find ~/.claude/plugins/cache -path "*/tendercopilot/*/scripts/plagiarism_core.py" 2>/dev/null | sort | tail -1)
python3 "$SCRIPT" "{target_folder}"
```

> **注意**：不要向用户展示正在运行的 Python 代码，除非发生错误。若 `SCRIPT` 为空（脚本未找到），告知用户重新安装插件：`claude /plugin install tendercopilot@tendercopilot`。

脚本将返回 JSON 数据，包含以下字段：
- `status`：`"success"` 或错误信息
- `scanned_count`：扫描文件总数
- `valid_count`：成功提取内容的文件数
- `pairs`：文件对列表，每项含 `file_a`、`file_b`、`score`（0–1）、`level`（High/Medium/Low）

### 步骤 3：分析与报告生成

获取 JSON 后，扮演"文档审计专家"角色，生成 Markdown 格式报告。**不要直接输出原始 JSON。**

#### 报告生成逻辑

- **高风险**（`level: "High"` 或相似度 > 0.7）：使用 🚨 标出，给出明确建议（如"建议人工复核后差异化修改"）。
- **中等风险**（`level: "Medium"`）：以表格形式列出。
- **无高风险**：明确告知用户"文档原创度良好"。

#### 报告模板

```markdown
## 📑 文档查重分析报告

**检测路径**: `{target_folder}`
**扫描文件数**: {scanned_count} 份
**有效提取**: {valid_count} 份

---

### ⚠️ 重点关注（相似度 > 70%）

（无高风险项时写"无"；有则按以下格式列出：）

🚨 **{file_a}** ↔ **{file_b}**
- 相似度：**{score}%**
- 建议：{根据相似度给出的简短建议}

---

### ℹ️ 详细比对表

（无其他重复时省略此节）

| 文件 A | 文件 B | 相似度 | 评级 |
| :--- | :--- | :--- | :--- |
| {file_a} | {file_b} | {score}% | {level} |
```

---

## 异常处理

| 错误类型 | 处理方式 |
|---------|---------|
| 文件数不足（< 2 个） | 通俗告知用户需补充文件 |
| 文件内容为空（纯图片/加密文档） | 告知用户文件无法提取文本 |
| Python 库缺失 | 提示用户运行 `pip install python-docx scikit-learn` |

---

## 依赖要求

- Python 3
- `python-docx`：读取 Word 文档
- `scikit-learn`：TF-IDF 向量化与余弦相似度计算

安装依赖：
```bash
pip install python-docx scikit-learn
```
