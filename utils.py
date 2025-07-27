# 工具类
import uuid
import yaml
import os
import logging
from typing import Dict, Any, List
import requests
from config import TestConfig

class TestUtils:
    """测试工具类"""
    
    @staticmethod
    def generate_request_uuid() -> str:
        """生成请求UUID"""
        return f"{str(uuid.uuid4()).replace('-', '')[:20]}-{str(uuid.uuid4()).replace('-', '')[:4]}"
    
    @staticmethod
    def load_test_data(yaml_file: str) -> Dict[str, Any]:
        """加载YAML测试数据"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, yaml_file)
        
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data
        except Exception as e:
            logging.error(f"加载测试数据失败: {e}")
            raise
    
    @staticmethod
    def make_api_request(url: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        """发送API请求"""
        if headers is None:
            headers = TestConfig.get_request_headers()
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=data,
                timeout=TestConfig.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API请求失败: {e}")
            raise
    
    @staticmethod
    def validate_response_structure(response: Dict[str, Any]) -> bool:
        """验证响应结构"""
        required_fields = ["RetCode", "Action"]
        return all(field in response for field in required_fields)
    
    @staticmethod
    def compare_eip_data(expected: Dict[str, Any], actual: Dict[str, Any]) -> List[str]:
        """比较EIP数据，返回差异列表"""
        differences = []
        
        for key, expected_value in expected.items():
            if key not in actual:
                differences.append(f"缺少字段: {key}")
                continue
            
            actual_value = actual[key]
            
            if expected_value is None and actual_value is not None:
                differences.append(f"字段 {key} 应该为None，实际为: {actual_value}")
            elif expected_value is not None and actual_value != expected_value:
                differences.append(f"字段 {key} 不匹配，期望: {expected_value}，实际: {actual_value}")
        
        return differences 