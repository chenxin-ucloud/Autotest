import pytest
import logging
from utils import TestUtils
from config import TestConfig

# 配置日志，持久存储到文件
import os

log_dir = getattr(TestConfig, "LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "test_describe_eip.log")

logging.basicConfig(
    level=getattr(logging, TestConfig.LOG_LEVEL),
    format=TestConfig.LOG_FORMAT,
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestDescribeEIP:
    """DescribeEIP接口测试类"""
    
    @pytest.fixture(scope="class")
    def test_data(self):
        """加载YAML格式测试数据"""
        return TestUtils.load_test_data("test_describe_eip.yml")
    
    @pytest.fixture(scope="class")
    def config(self, test_data):
        """从测试数据中获取配置信息"""
        return test_data["config"]
    
    def test_describe_eip_smoke(self, test_data, config):
        """冒烟测试，包含not_expected字段断言"""
        test_cases = test_data["test_cases"]
        
        for case in test_cases:
            logger.info(f"执行测试用例: {case['name']} (ID: {case['case_id']})")
            
            # 准备请求数据
            request_data = case["request_data"].copy()
            if "request_uuid" not in request_data:
                request_data["request_uuid"] = TestUtils.generate_request_uuid()
            
            # 合并基础参数
            base_params = TestConfig.get_base_params()
            request_data.update(base_params)
            
            # 发送请求
            try:
                response = TestUtils.make_api_request(
                    url=config["base_url"],
                    data=request_data,
                    headers=config["headers"]
                )
            except Exception as e:
                pytest.fail(f"请求发送失败: {str(e)}")                  
            
            # 基础断言
            expected = case["expected"]
            assert response["RetCode"] == expected["RetCode"], \
                f"RetCode断言失败，期望: {expected['RetCode']}，实际: {response['RetCode']}"
            assert response["Action"] == expected["Action"], \
                f"Action断言失败，期望: {expected['Action']}，实际: {response['Action']}"

            # 处理not_expected断言
            if "not_expected" in case:
                self.assert_not_expected(response, case["not_expected"])
    
    def assert_not_expected(self, response: dict, not_expected: dict):
        """断言响应中不包含指定字段"""
        for key, value in not_expected.items():
            # 检查顶层字段是否存在
            if key in response:
                # 如果是嵌套结构，递归检查
                if isinstance(value, dict) and isinstance(response[key], (dict, list)):
                    # 处理列表类型的响应字段
                    if isinstance(response[key], list):
                        for item in response[key]:
                            self.assert_nested_not_expected(item, value)
                    else:  # 处理字典类型的响应字段
                        self.assert_nested_not_expected(response[key], value)
                else:
                    pytest.fail(f"响应中不应包含字段: {key}")
    
    def assert_nested_not_expected(self, response_part: dict, not_expected_part: dict):
        """递归断言嵌套结构中不包含指定字段"""
        for key, value in not_expected_part.items():
            if key in response_part:
                if isinstance(value, dict) and isinstance(response_part[key], dict):
                    self.assert_nested_not_expected(response_part[key], value)
                else:
                    pytest.fail(f"响应中不应包含字段: {key}")


if __name__ == "__main__":
    pytest.main(["-vs", "Ftest_describe_eip.py"])