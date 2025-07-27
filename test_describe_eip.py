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
        return TestUtils.load_test_data("test_describe_eip.yml")
    
    @pytest.fixture(scope="class")
    def config(self):
        """获取配置信息"""
        return TestUtils.load_test_data("test_describe_eip.yml")["config"]
    
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
            
            # EIPSet详细断言
            if "EIPSet" in expected:
                self._validate_eip_set(response, expected["EIPSet"], case["name"])
    
    def _validate_eip_set(self, response: Dict[str, Any], expected_eip_set: List[Dict], case_name: str):
        """验证EIPSet数据"""
        actual_eip_set = response.get("EIPSet", [])
        
        if not expected_eip_set:
            # 期望EIPSet为空的情况
            assert len(actual_eip_set) == 0, f"{case_name}: EIPSet应该为空"
            return
        
        # 验证EIPSet不为空
        assert len(actual_eip_set) >= 1, f"{case_name}: EIPSet为空，未查询到EIP信息"
        
        # 验证指定的EIP数据
        for expected_eip in expected_eip_set:
            if "EIPId" in expected_eip:
                target_eip_id = expected_eip["EIPId"]
                matched_eip = next(
                    (eip for eip in actual_eip_set if eip.get("EIPId") == target_eip_id),
                    None
                )
                assert matched_eip is not None, f"{case_name}: 未找到EIPId: {target_eip_id}的记录"
                
                # 验证EIP详细字段
                self._validate_eip_fields(matched_eip, expected_eip, case_name)
    
    def _validate_eip_fields(self, actual_eip: Dict[str, Any], expected_eip: Dict[str, Any], case_name: str):
        """验证EIP字段"""
        differences = TestUtils.compare_eip_data(expected_eip, actual_eip)
        
        if differences:
            error_msg = f"{case_name}: EIP字段验证失败:\n" + "\n".join(differences)
            pytest.fail(error_msg)
    
    @pytest.mark.parametrize("case_id", ["TC001", "TC002", "TC003"])
    def test_describe_eip_normal_scenarios(self, test_data, config, case_id):
        """正常场景参数化测试"""
        test_cases = test_data["test_cases"]
        case = next((c for c in test_cases if c["case_id"] == case_id), None)
        
        if not case:
            pytest.skip(f"未找到测试用例: {case_id}")
        
        logger.info(f"执行参数化测试: {case['name']}")
        
        # 准备请求数据
        request_data = case["request"]["data"].copy()
        request_data["request_uuid"] = TestUtils.generate_request_uuid()
        request_data.update(TestConfig.get_base_params())
        
        # 发送请求
        response = TestUtils.make_api_request(
            url=config["base_url"],
            data=request_data,
            headers=config["headers"]
        )
        
        # 验证响应
        expected = case["expected"]
        assert response["RetCode"] == expected["RetCode"]
        assert response["Action"] == expected["Action"]
        
        # 验证统计字段
        if "TotalCount" in expected:
            total_count = response.get("TotalCount", 0)
            if isinstance(expected["TotalCount"], str) and expected["TotalCount"].startswith(">="):
                min_count = int(expected["TotalCount"][2:])
                assert total_count >= min_count, f"TotalCount应该大于等于{min_count}"
            else:
                assert total_count == expected["TotalCount"]
    
    @pytest.mark.parametrize("case_id", ["TC004", "TC005", "TC006"])
    def test_describe_eip_error_scenarios(self, test_data, config, case_id):
        """异常场景参数化测试"""
        test_cases = test_data["test_cases"]
        case = next((c for c in test_cases if c["case_id"] == case_id), None)
        
        if not case:
            pytest.skip(f"未找到测试用例: {case_id}")
        
        logger.info(f"执行异常场景测试: {case['name']}")
        
        # 准备请求数据
        request_data = case["request"]["data"].copy()
        request_data["request_uuid"] = TestUtils.generate_request_uuid()
        request_data.update(TestConfig.get_base_params())
        
        # 发送请求
        response = TestUtils.make_api_request(
            url=config["base_url"],
            data=request_data,
            headers=config["headers"]
        )
        
        # 验证响应
        expected = case["expected"]
        assert response["RetCode"] == expected["RetCode"]
        assert response["Action"] == expected["Action"]
    
    def test_describe_eip_performance(self, config):
        """性能测试"""
        logger.info("执行性能测试")
        
        request_data = {
            "Action": "DescribeEIP",
            "Limit": 100,
            "request_uuid": TestUtils.generate_request_uuid()
        }
        request_data.update(TestConfig.get_base_params())
        
        import time
        start_time = time.time()
        
        response = TestUtils.make_api_request(
            url=config["base_url"],
            data=request_data,
            headers=config["headers"]
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # 性能断言
        assert response_time < 5.0, f"响应时间过长: {response_time:.2f}秒"
        assert response["RetCode"] == 0, "性能测试中API调用失败"
        
        logger.info(f"性能测试完成，响应时间: {response_time:.2f}秒")

if __name__ == "__main__":
    pytest.main([
        "-v", 
        "test_describe_eip.py",
        "--html=reports/report.html",
        "--json=reports/report.json",
        "--self-contained-html"
    ])