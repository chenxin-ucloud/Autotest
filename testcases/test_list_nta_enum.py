import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import requests
import allure
import json
from comms.json_utils import JsonDataLoader
from comms.log_utils import logger
from comms.config import prepare_request_body, API_CONFIG, COMMON_HEADERS


# 加载JSON测试数据
json_data = JsonDataLoader.load_json("datas/ListNTAEnum.json")
test_cases = JsonDataLoader.get_test_cases(json_data)

# ListNTAEnum 接口测试类
@allure.feature("ListNTAEnum 接口测试")
class TestListNTAEnum:
    @classmethod
    def setup_class(cls):
        """测试类初始化，获取API配置"""
        cls.base_url = API_CONFIG['base_url']
        cls.method = API_CONFIG['method']
        cls.timeout = API_CONFIG['timeout']
        cls.headers = COMMON_HEADERS

    @allure.severity("critical")
    @allure.description("ListNTAEnum 接口功能测试")
    @pytest.mark.parametrize("case", test_cases, ids=[case.get('case_id', '') for case in test_cases])
    def test_list_nta_enum_smoke(self, case):
        """
        测试 ListNTAEnum API 接口
        
        测试步骤：
        1. 准备请求数据和期望结果
        2. 生成带签名的请求体
        3. 发送 POST 请求
        4. 断言验证返回结果
        """
        # 1. 准备请求数据
        request_data = case.get('request_data', {})
        expected = case.get('expected', {})
        case_id = case.get('case_id', 'Unknown')
        case_name = case.get('name', 'Unknown')

        # 2. 生成带签名的请求体
        signed_request_data = prepare_request_body(request_data)

        # 3. 记录日志和Allure报告信息
        logger.info(f"{'='*60}")
        logger.info(f"测试用例 [{case_id}]: {case_name}")
        logger.info(f"API地址: {self.base_url}")
        logger.info(f"请求方法: {self.method}")
        logger.info(f"原始参数: {request_data}")
        logger.info(f"签名后参数: {signed_request_data}")

        allure.dynamic.title(case_name)
        allure.attach(body=self.base_url, name='接口地址', attachment_type=allure.attachment_type.TEXT)
        allure.attach(body=self.method, name='请求方法', attachment_type=allure.attachment_type.TEXT)
        allure.attach(body=json.dumps(request_data, indent=2, ensure_ascii=False), 
                     name='原始请求参数', attachment_type=allure.attachment_type.JSON)
        allure.attach(body=json.dumps(signed_request_data, indent=2, ensure_ascii=False), 
                     name='签名后请求参数', attachment_type=allure.attachment_type.JSON)

        # 4. 发送请求
        logger.info(f"发送请求...")
        try:
            response = requests.post(
                url=self.base_url,
                json=signed_request_data,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            allure.attach(body=str(e), name='请求异常', attachment_type=allure.attachment_type.TEXT)
            raise

        # 5. 记录响应
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"响应结果: {response_data}")
        allure.attach(body=json.dumps(response_data, indent=2, ensure_ascii=False), 
                     name='响应结果', attachment_type=allure.attachment_type.JSON)

        # 6. 断言验证
        try:
            # 验证返回码
            assert 'RetCode' in response_data, "响应中缺少RetCode字段"
            assert response_data['RetCode'] == expected['RetCode'], \
                f"返回码不符，期望: {expected['RetCode']}, 实际: {response_data['RetCode']}"
            
            # 验证Action字段
            assert 'Action' in response_data, "响应中缺少Action字段"
            assert response_data['Action'] == expected['Action'], \
                f"Action不符，期望: {expected['Action']}, 实际: {response_data['Action']}"
            
            logger.info(f"✓ 测试用例 [{case_id}]: {case_name} 执行通过")
            allure.attach(body=f"测试通过，返回码：{response_data['RetCode']}", 
                         name='测试结果', attachment_type=allure.attachment_type.TEXT)
            
        except AssertionError as e:
            logger.error(f"✗ 测试用例 [{case_id}]: {case_name} 执行失败")
            logger.error(f"失败原因: {str(e)}")
            allure.attach(body=f"测试失败: {str(e)}", 
                         name='测试结果', attachment_type=allure.attachment_type.TEXT)
            raise


class TestListNTAEnumAdditional:
    """额外的测试场景"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        cls.base_url = API_CONFIG['base_url']
        cls.method = API_CONFIG['method']
        cls.timeout = API_CONFIG['timeout']
        cls.headers = COMMON_HEADERS

    @allure.severity("normal")
    @allure.description("验证签名功能正常工作")
    def test_signature_is_included(self):
        """验证请求中包含了PublicKey和Signature"""
        request_data = {'Action': 'ListNTAEnum'}
        signed_data = prepare_request_body(request_data)
        
        logger.info("验证签名字段...")
        assert 'PublicKey' in signed_data, "请求体中缺少PublicKey字段"
        assert 'Signature' in signed_data, "请求体中缺少Signature字段"
        assert 'Action' in signed_data, "请求体中缺少Action字段"
        
        logger.info(f"PublicKey: {signed_data['PublicKey']}")
        logger.info(f"Signature: {signed_data['Signature']}")
        logger.info("✓ 签名字段验证通过")

    @allure.severity("normal")
    @allure.description("验证API配置信息完整")
    def test_api_config_complete(self):
        """验证API配置信息完整性"""
        logger.info("验证API配置...")
        assert 'base_url' in API_CONFIG, "配置中缺少base_url"
        assert 'method' in API_CONFIG, "配置中缺少method"
        assert 'timeout' in API_CONFIG, "配置中缺少timeout"
        
        assert API_CONFIG['base_url'].startswith('http'), "base_url格式不正确"
        assert API_CONFIG['method'].upper() in ['GET', 'POST', 'PUT', 'DELETE'], "method不支持"
        assert isinstance(API_CONFIG['timeout'], int), "timeout必须是整数"
        
        logger.info(f"Base URL: {API_CONFIG['base_url']}")
        logger.info(f"Method: {API_CONFIG['method']}")
        logger.info(f"Timeout: {API_CONFIG['timeout']}s")
        logger.info("✓ API配置验证通过")

    @allure.severity("normal")
    @allure.description("验证请求头配置")
    def test_common_headers_config(self):
        """验证请求头配置"""
        logger.info("验证请求头配置...")
        assert 'Content-Type' in COMMON_HEADERS, "请求头缺少Content-Type"
        assert COMMON_HEADERS['Content-Type'] == 'application/json', "Content-Type应为application/json"
        
        logger.info(f"Content-Type: {COMMON_HEADERS['Content-Type']}")
        logger.info(f"包含Cookie: {'Cookie' in COMMON_HEADERS}")
        logger.info("✓ 请求头配置验证通过")
