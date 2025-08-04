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
        """加载测试数据"""
        return TestUtils.load_test_data("test_describe_eip.json")
    
    @pytest.fixture(scope="class")
    def config(self):
        """获取配置信息"""
        return TestUtils.load_test_data("test_describe_eip.json")["config"]
    
    def test_describe_eip_smoke(self, test_data, config):
        """冒烟测试"""
        test_cases = test_data["test_cases"]
        
        for case in test_cases:
            logger.info(f"执行测试用例: {case['name']}")
            
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

            # 返回字段断言
            if case['case_id'] == "TC001":
                assert "ResourceEipDirectModeType" and "SubResourceEipDirectModeType" not in response, \
                    f"用例:{case['name']}响应中不应包含ResourceEipDirectModeType和SubResourceEipDirectModeType字段"
            

if __name__ == "__main__":
    pytest.main(["-vs", "test_describe_eip.py"])