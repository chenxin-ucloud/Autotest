import pytest
import logging
from typing import Dict, Any, List
from utils import TestUtils
from config import TestConfig

# 配置日志
logging.basicConfig(
    level=getattr(logging, TestConfig.LOG_LEVEL),
    format=TestConfig.LOG_FORMAT
)
logger = logging.getLogger(__name__)

class TestDescribeEIP:
    """DescribeEIP接口测试类"""
    
    @pytest.fixture(scope="class")
    def test_data(self):
        """加载测试数据"""
        return TestUtils.load_test_data("test_describe_eip.json")
    
    @pytest.fixture(scope="class")
    def config(self):
        """获取配置信息"""
        return TestUtils.load_test_data("test_describe_eip.json")["config"]
    
    def test_describe_eip_basic(self, test_data, config):
        """基础功能测试"""
        test_cases = test_data["test_cases"]
        
        for case in test_cases:
            logger.info(f"执行测试用例: {case['name']}")
            
            # 准备请求数据
            request_data = case["request"]["data"].copy()
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
            
            # 验证响应结构
            assert TestUtils.validate_response_structure(response), "响应结构不正确"
            
            # 基础断言
            expected = case["expected"]
            assert response["RetCode"] == expected["RetCode"], \
                f"RetCode断言失败，期望: {expected['RetCode']}，实际: {response['RetCode']}"
            assert response["Action"] == expected["Action"], \
                f"Action断言失败，期望: {expected['Action']}，实际: {response['Action']}"
            # 返回字段断言
            if case['case_id'] != "TC001":
                assert "UnbindCount" not in response, \
                    f"用例:{case['name']}响应中不应包含UnbindCount字段"
    