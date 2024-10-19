import os

def save_markdown_from_model_output(output, base_dir="markdown_output", start_index=1):
    """
    根据大模型返回的内容，拆分并生成带数字前缀的 Markdown 文件。
    """
    os.makedirs(base_dir, exist_ok=True)
    knowledge_points = output.split("|||")

    for i, point in enumerate(knowledge_points, start=start_index):
        # 去除首尾空行
        point = point.strip()

        # 打印调试信息，帮助用户排查问题
        print(f"正在处理第 {i} 个知识点...")

        # 检查是否存在 'aliases:' 行
        alias_line = next((line for line in point.split("\n") if line.startswith("aliases:")), None)
        if alias_line is None:
            print(f"错误：模型输出内容缺失 'aliases:' 字段。\n输出内容:\n{point}")
            raise ValueError("无法找到 'aliases:' 行，请检查模型输出格式。")

        # 提取 alias 作为文件名
        alias = alias_line.split(":")[1].strip()

        # 添加数字前缀到文件名
        file_name = f"{i:02d}_{alias}.md"
        file_path = os.path.join(base_dir, file_name)

        # 保存为 Markdown 文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(point)
