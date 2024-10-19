import os
import yaml
from src.config_loader import load_config
from src.pdf_parser import convert_toc_pages_to_images
from src.folder_generator import generate_folders_from_toc
from src.content_splitter import split_content_by_toc
from src.yaml_utils import regenerate_toc_with_retry


def user_confirmation(toc_path):
    """等待用户确认目录文件，或上传新的目录文件。"""
    print(f"目录文件已生成：{toc_path}")
    print("请检查生成的目录文件是否正确，或者上传自定义目录文件（按路径输入）。")

    while True:
        choice = input("是否确认使用该目录文件？(y/n) 或输入自定义目录文件路径：").strip()

        if choice.lower() == 'y':
            print("确认使用生成的目录文件，继续执行...")
            return toc_path  # 使用生成的目录文件
        elif choice.lower() == 'n':
            print("用户拒绝使用目录文件，流程终止。")
            exit(0)  # 用户拒绝，终止程序
        elif os.path.exists(choice):
            print(f"使用用户上传的目录文件：{choice}")
            return choice  # 使用用户上传的目录文件
        else:
            print("输入无效，请重新输入。")


def main():
    """主流程：从 PDF 中提取目录并拆分正文内容。"""
    config = load_config()
    storage_dir = config["storage"]["base_dir"]

    # 从配置中获取书本参数
    book_config = config["book"]
    pdf_file = book_config["pdf_file"]
    toc_start = book_config["toc_start"]
    toc_end = book_config["toc_end"]
    content_start = book_config["content_start"]
    content_end = book_config["content_end"]

    # 1. 将目录页转换为图像，并传递给大模型识别目录
    toc_image_paths = convert_toc_pages_to_images(pdf_file, toc_start, toc_end,
                                                  os.path.join(storage_dir, "toc_images"))
    print('完成目录页转换为图像')

    # 2. 循环生成目录结构，确保合法性
    toc_yaml, toc_data = regenerate_toc_with_retry(toc_image_paths, config)
    print('目录页转换为yml格式')

    # 3. 保存目录结构为 YAML 文件
    toc_path = os.path.join(storage_dir, "toc.yml")
    with open(toc_path, "w", encoding="utf-8") as f:
        f.write(toc_yaml)
    print(f"目录结构已保存至 {toc_path}")

    # 4. 用户确认目录文件或上传自定义目录文件
    confirmed_toc_path = user_confirmation(toc_path)

    # 5. 加载确认后的目录文件
    with open(confirmed_toc_path, "r", encoding="utf-8") as f:
        toc_data = yaml.safe_load(f)

    # 6. 根据目录结构生成文件夹
    generate_folders_from_toc(toc_data, os.path.join(storage_dir, "content"))
    print('完成目录结构生成文件夹')

    # 7. 拆分正文内容并生成 Markdown 文件
    split_content_by_toc(pdf_file, toc_data, os.path.join(storage_dir, "content"), config)
    print('完成拆书，学习愉快')


if __name__ == "__main__":
    main()
