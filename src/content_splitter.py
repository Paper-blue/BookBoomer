import os
from tqdm import tqdm
from src.pdf_parser import convert_pdf_to_images
from src.model_interface import generate_image_analysis
from src.markdown_generator import save_markdown_from_model_output

def process_leaf_folder(pdf_file, start_page, end_page, folder_path, config, content_start):
    """处理最底层文件夹，并生成 Markdown 文件。"""
    adjusted_start = start_page + (content_start - 1)
    adjusted_end = end_page + (content_start - 1)

    images = convert_pdf_to_images(pdf_file, adjusted_start, adjusted_end,
                                   os.path.join(folder_path, "images"))

    try:
        print(f"正在生成 {folder_path} 的 Markdown 文件...")
        model_output = generate_image_analysis(images, config)
        save_markdown_from_model_output(model_output, folder_path)
        print(f"成功生成 {folder_path} 的 Markdown 文件！")
    except ValueError as e:
        print(f"错误：{e}。无法生成 {folder_path} 的内容。")

def split_subchapters_recursive(pdf_file, chapters, base_dir, config, content_start, prefix=""):
    """递归处理章节和子章节，将 Markdown 文件放在最底层文件夹中。"""
    for index, chapter in enumerate(chapters, start=1):
        chapter_name = chapter["章节名"]
        chapter_prefix = f"{prefix}{index}-"
        folder_name = f"{chapter_prefix}{chapter_name}"
        folder_path = os.path.join(base_dir, folder_name)

        if "子章节" in chapter:
            # 递归处理子章节
            split_subchapters_recursive(pdf_file, chapter["子章节"], folder_path, config, content_start, chapter_prefix)
        else:
            # 处理最底层文件夹
            start_page, end_page = chapter["页码范围"]
            process_leaf_folder(pdf_file, start_page, end_page, folder_path, config, content_start)

def split_content_by_toc(pdf_file, toc_data, storage_dir, config):
    """根据目录结构递归处理，并将 Markdown 文件存储在最底层文件夹中。"""
    content_start = config["book"]["content_start"]

    with tqdm(total=len(toc_data["目录结构"]), desc="生成章节内容", unit="章") as pbar:
        split_subchapters_recursive(pdf_file, toc_data["目录结构"], storage_dir, config, content_start)
        pbar.update(1)
