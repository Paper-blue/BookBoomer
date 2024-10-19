from pdf2image import convert_from_path
import os
import base64
from io import BytesIO

def convert_pdf_to_images(pdf_file, start_page, end_page, output_dir="pdf_images"):
    """
    将指定页码范围内的 PDF 转换为图像，并返回 Base64 编码的字符串列表。
    同时将生成的图像保存到指定文件夹。
    """
    os.makedirs(output_dir, exist_ok=True)  # 创建输出目录

    images = convert_from_path(pdf_file, first_page=start_page, last_page=end_page)
    base64_images = []

    for idx, image in enumerate(images, start=start_page):
        # 保存图像文件
        image_path = os.path.join(output_dir, f"page_{idx}.jpg")
        image.save(image_path, "JPEG")

        # 将图像编码为 Base64 并存入列表
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        base64_images.append(base64_image)

    return base64_images

def convert_toc_pages_to_images(pdf_file, toc_start, toc_end, output_dir="toc_images"):
    """
    将目录页转换为图像，并保存到指定文件夹。
    返回生成的图像路径列表。
    """
    os.makedirs(output_dir, exist_ok=True)

    images = convert_from_path(pdf_file, first_page=toc_start, last_page=toc_end)
    image_paths = []

    for i, image in enumerate(images, start=toc_start):
        # 保存图像文件
        image_path = os.path.join(output_dir, f"toc_page_{i}.jpg")
        image.save(image_path, "JPEG")
        image_paths.append(image_path)

    return image_paths
