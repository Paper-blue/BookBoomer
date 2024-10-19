import yaml

def load_config(config_path="config.yaml"):
    """加载配置文件并返回配置字典。"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
