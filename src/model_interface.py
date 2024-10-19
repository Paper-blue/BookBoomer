import base64
import os
import re
import yaml

from openai import OpenAI

def initialize_client(config):
    """初始化 OpenAI 客户端，并返回客户端实例。"""
    return OpenAI(api_key=config["model"]["api_key"])

def generate_image_analysis(images, config):
    """调用大语言模型分析图像，并返回模型生成的内容。"""
    client = initialize_client(config)
    prompt = config["prompts"]["knowledge_point_prompt"]

    # 构建图像和文本消息内容
    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]

    # 将每张图像的 Base64 编码数据添加为独立的消息对象
    for image in images:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
                }
            }
        )

    # 构建 API 的消息格式
    messages = [{"role": "user", "content": content}]

    # 调用模型接口
    response = client.chat.completions.create(
        model=config["model"]["name"],
        messages=messages,
        max_tokens=config["model"]["max_tokens"]
    )

    return response.choices[0].message.content.strip()


def clean_yaml_output(yaml_content):
    """清洗大模型返回的 YAML 内容，去除多余的标识符。"""
    # 移除 Markdown 代码块的标识符（如 ```yaml）
    cleaned_content = re.sub(r"```(?:yaml)?", "", yaml_content).strip()
    return cleaned_content

def generate_toc_structure(image_paths, config):
    """调用大语言模型识别目录，并返回清理后的 YAML 格式的目录结构。"""
    client = initialize_client(config)
    prompt = config["prompts"]["toc_prompt"]

    # 构建消息数组：包含提示词和目录页的图片数据
    content = [{"type": "text", "text": prompt}]
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                }
            )

    messages = [{"role": "user", "content": content}]

    # 调用模型接口
    response = client.chat.completions.create(
        model=config["model"]["name"],
        messages=messages,
        max_tokens=config["model"]["max_tokens"]
    )

    toc_yaml_raw = response.choices[0].message.content.strip()
    toc_yaml_cleaned = clean_yaml_output(toc_yaml_raw)

    return toc_yaml_cleaned