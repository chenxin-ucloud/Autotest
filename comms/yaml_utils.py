import yaml
from typing import Dict, List


class YamlDataLoader:
    @staticmethod
    def load_yaml(file_path: str) -> Dict:
        """加载YAML文件并返回字典数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML文件不存在: {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML文件格式错误: {file_path}, 错误: {str(e)}")

    @staticmethod
    def get_test_cases(yaml_data: Dict) -> List[Dict]:
        """从YAML数据中提取测试用例列表"""
        return yaml_data.get("test_cases", [])

    @staticmethod
    def get_config(yaml_data: Dict) -> Dict:
        """从YAML数据中提取配置信息"""
        return yaml_data.get("config", {})