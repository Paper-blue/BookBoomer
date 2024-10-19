import os

def generate_folders_from_toc(toc_data, base_dir):
    """根据目录结构生成文件夹路径。"""
    def create_folder_recursive(chapters, parent_dir, prefix=""):
        """递归创建文件夹结构。"""
        for index, chapter in enumerate(chapters, start=1):
            chapter_name = chapter["章节名"]
            chapter_prefix = f"{prefix}{index}-"
            folder_name = f"{chapter_prefix}{chapter_name}"
            folder_path = os.path.join(parent_dir, folder_name)

            os.makedirs(folder_path, exist_ok=True)

            # 如果有子章节，则递归创建
            if "子章节" in chapter:
                create_folder_recursive(chapter["子章节"], folder_path, chapter_prefix)

    create_folder_recursive(toc_data["目录结构"], base_dir)
