import sys
import os
import glob
import json
import warnings

# 抑制 sklearn 可能产生的警告，防止污染 JSON 输出
warnings.filterwarnings("ignore")

try:
    from docx import Document
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError as e:
    # 如果缺少库，以 JSON 格式报错
    error_msg = {
        "error": "Missing Dependencies",
        "message": f"缺少必要的 Python 库: {str(e)}。请运行 pip install python-docx scikit-learn"
    }
    print(json.dumps(error_msg, ensure_ascii=False))
    sys.exit(1)

def read_docx(file_path):
    """
    读取 docx 文件内容。
    为了准确性，过滤掉过短的段落（如页码、简单的标题）。
    """
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            text = para.text.strip()
            # 仅保留长度大于 5 的段落，减少页眉页脚噪音
            if len(text) > 5:
                full_text.append(text)
        return "\n".join(full_text)
    except Exception:
        return ""

def main():
    # 1. 参数解析
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # 容错：如果用户输入的是文件而不是目录，取其父目录
    if os.path.isfile(target_dir):
        target_dir = os.path.dirname(target_dir)

    # 2. 扫描文件
    search_pattern = os.path.join(target_dir, "*.docx")
    files = glob.glob(search_pattern)
    
    # 确保只处理文件名（不含路径），用于展示
    file_map = {os.path.basename(f): f for f in files}
    filenames = list(file_map.keys())

    # 3. 前置检查
    if len(files) < 2:
        result = {
            "error": "Insufficient Files",
            "message": f"在路径 '{target_dir}' 下只找到了 {len(files)} 个 .docx 文件，至少需要 2 个才能进行查重。",
            "scanned_count": len(files),
            "pairs": []
        }
        print(json.dumps(result, ensure_ascii=False))
        return

    # 4. 读取内容
    documents = []
    valid_filenames = []
    
    for fname in filenames:
        content = read_docx(file_map[fname])
        if content:
            documents.append(content)
            valid_filenames.append(fname)

    if len(documents) < 2:
        result = {
            "error": "Empty Content",
            "message": "找到了文件，但无法提取有效文本（可能是纯图片文档或加密文档）。",
            "scanned_count": len(files),
            "pairs": []
        }
        print(json.dumps(result, ensure_ascii=False))
        return

    # 5. 核心算法 (TF-IDF + Cosine Similarity)
    # analyzer='char' 对于中英文混合非常稳健，不需要复杂的分词库
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
    tfidf_matrix = vectorizer.fit_transform(documents)
    sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 6. 构建结果数据
    pairs_data = []
    count = len(valid_filenames)
    
    for i in range(count):
        for j in range(i + 1, count):
            score = sim_matrix[i][j]
            
            # 过滤掉相似度过低的结果，保持报告整洁 (阈值 0.2)
            if score > 0.2:
                # 评级逻辑
                if score > 0.7:
                    level = "High"
                elif score > 0.4:
                    level = "Medium"
                else:
                    level = "Low"

                pairs_data.append({
                    "file_a": valid_filenames[i],
                    "file_b": valid_filenames[j],
                    "score": round(score, 4), # 保留4位小数，例如 0.8521
                    "level": level
                })

    # 按相似度从高到低排序
    pairs_data.sort(key=lambda x: x["score"], reverse=True)

    # 7. 输出最终 JSON
    final_output = {
        "status": "success",
        "directory": target_dir,
        "scanned_count": len(files),
        "valid_count": len(valid_filenames),
        "pairs": pairs_data
    }

    print(json.dumps(final_output, ensure_ascii=False))

if __name__ == "__main__":
    main()