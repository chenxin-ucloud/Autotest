import json
from typing import Dict, List


class JsonDataLoader:
    @staticmethod
    def load_json(file_path: str) -> Dict:
        """加载JSON文件并返回字典数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON文件不存在: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"JSON文件格式错误: {file_path}")

    @staticmethod
    def get_test_cases(json_data: Dict) -> List[Dict]:
        """从JSON数据中提取测试用例列表"""
        return json_data.get("test_cases", [])

    @staticmethod
    def get_config(api_name: str) -> Dict:
        """从config.py中获取指定API的配置信息"""
        # 延迟导入避免循环导入
        from comms.config import get_api_config
        return get_api_config(api_name)

