import os
import base64
import os
from pdf2image import convert_from_path


def pdf_to_images(pdf_path, output_dir="images"):
    """将 PDF 文件转换为图像，并保存在指定目录中。"""
    os.makedirs(output_dir, exist_ok=True)

    # 将 PDF 的每一页转换为图像
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{i + 1}.jpg")
        image.save(image_path, "JPEG")
        image_paths.append(image_path)

    return image_paths


def encode_image(image_path):
    """将图像文件编码为 base64 字符串。"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def ensure_directory_exists(path):
    """确保给定路径的目录存在，如果不存在则创建。"""
    os.makedirs(path, exist_ok=True)

