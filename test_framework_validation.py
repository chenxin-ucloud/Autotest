#!/usr/bin/env python3
"""
测试框架验证脚本
用于验证测试框架的完整性，不依赖外部API
"""
import pytest
import yaml
import os
from utils import TestUtils
from config import TestConfig

class TestFrameworkValidation:
    """测试框架验证类"""
    
    def test_config_loading(self):
        """测试配置加载"""
        assert TestConfig.BASE_URL is not None
        assert TestConfig.TIMEOUT > 0
        assert isinstance(TestConfig.get_request_headers(), dict)
        assert isinstance(TestConfig.get_base_params(), dict)
        print("✓ 配置加载测试通过")
    
    def test_utils_functions(self):
        """测试工具函数"""
        # 测试UUID生成
        uuid1 = TestUtils.generate_request_uuid()
        uuid2 = TestUtils.generate_request_uuid()
        assert len(uuid1) > 0
        assert uuid1 != uuid2
        print("✓ UUID生成测试通过")
        
        # 测试YAML数据加载
        test_data = TestUtils.load_test_data("test_describe_eip.yml")
        assert "config" in test_data
        assert "test_cases" in test_data
        assert len(test_data["test_cases"]) > 0
        print("✓ YAML数据加载测试通过")
        
        # 测试响应结构验证
        valid_response = {"RetCode": 0, "Action": "DescribeEIPResponse"}
        invalid_response = {"RetCode": 0}
        assert TestUtils.validate_response_structure(valid_response) == True
        assert TestUtils.validate_response_structure(invalid_response) == False
        print("✓ 响应结构验证测试通过")
        
        # 测试EIP数据比较
        expected = {"EIPId": "test-id", "Status": "used"}
        actual = {"EIPId": "test-id", "Status": "used"}
        differences = TestUtils.compare_eip_data(expected, actual)
        assert len(differences) == 0
        
        actual_different = {"EIPId": "test-id", "Status": "free"}
        differences = TestUtils.compare_eip_data(expected, actual_different)
        assert len(differences) > 0
        print("✓ EIP数据比较测试通过")
    
    def test_yaml_structure(self):
        """测试YAML文件结构"""
        test_data = TestUtils.load_test_data("test_describe_eip.yml")
        
        # 验证配置部分
        config = test_data["config"]
        assert "base_url" in config
        assert "timeout" in config
        assert "headers" in config
        print("✓ YAML配置结构测试通过")
        
        # 验证测试用例结构
        test_cases = test_data["test_cases"]
        for case in test_cases:
            assert "case_id" in case
            assert "name" in case
            assert "request" in case
            assert "expected" in case
            assert "data" in case["request"]
        print("✓ YAML测试用例结构测试通过")
    
    def test_test_data_content(self):
        """测试测试数据内容"""
        test_data = TestUtils.load_test_data("test_describe_eip.yml")
        test_cases = test_data["test_cases"]
        
        # 验证至少有一个正常场景测试
        normal_cases = [case for case in test_cases if case["case_id"] in ["TC001", "TC002", "TC003"]]
        assert len(normal_cases) >= 1
        
        # 验证至少有一个异常场景测试
        error_cases = [case for case in test_cases if case["case_id"] in ["TC004", "TC005", "TC006"]]
        assert len(error_cases) >= 1
        
        print("✓ 测试数据内容验证通过")
    
    def test_file_structure(self):
        """测试项目文件结构"""
        required_files = [
            "config.py",
            "utils.py", 
            "test_describe_eip.py",
            "test_describe_eip.yml",
            "pytest.ini",
            "requirements.txt",
            "run_tests.py",
            "README.md"
        ]
        
        for file_name in required_files:
            assert os.path.exists(file_name), f"缺少文件: {file_name}"
        
        # 验证reports目录
        assert os.path.exists("reports") or os.path.isdir("reports")
        
        print("✓ 项目文件结构验证通过")

if __name__ == "__main__":
    print("开始验证测试框架...")
    pytest.main(["-v", "test_framework_validation.py"])
    print("框架验证完成!") 