import yaml
from src.model_interface import generate_toc_structure

def load_and_validate_yaml(yaml_content):
    """解析 YAML 并验证格式是否正确，返回解析后的数据或抛出异常。"""
    try:
        toc_data = yaml.safe_load(yaml_content)
        if not isinstance(toc_data, dict) or "目录结构" not in toc_data:
            raise ValueError("YAML 格式不正确或缺少 '目录结构' 字段。")
        return toc_data
    except yaml.YAMLError as e:
        print(f"YAML 解析失败：{e}")
        raise

def regenerate_toc_with_retry(toc_image_paths, config):
    """
    循环调用模型生成目录结构，直到成功或达到最大重试次数。
    """
    max_attempts = config["retry"]["max_attempts"]

    for attempt in range(max_attempts):
        try:
            print(f"正在生成目录结构（第 {attempt + 1} 次尝试）...")
            toc_yaml = generate_toc_structure(toc_image_paths, config)
            toc_data = load_and_validate_yaml(toc_yaml)
            print("目录生成成功！")
            return toc_yaml, toc_data  # 成功时返回
        except (ValueError, yaml.YAMLError) as e:
            print(f"错误：{e}。")

    raise RuntimeError(f"超过最大重试次数 {max_attempts} 次，无法生成有效的目录结构。")
