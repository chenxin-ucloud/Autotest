import pytest
import requests
import allure
import json
from comms.json_utils import JsonDataLoader
from comms.log_utils import logger


# 加载JSON测试数据
json_data = JsonDataLoader.load_json("datas/describe_eip.json")
test_cases = JsonDataLoader.get_test_cases(json_data)
config = JsonDataLoader.get_config(json_data)

# DescribeEIP测试类
@allure.feature("DescribeEIP 接口测试")
class TestDescribeEIP:
    @allure.severity("critical")  # 为allure报告修改case优先级
    @allure.description("DescribeEIP 接口测试用例")  # 为allure报告添加描述(备注)
    @pytest.mark.parametrize("case", test_cases)  # 参数化JSON中的用例
    def test_describe_eip_smoke(self, case):
        # 1. 准备请求数据
        url = f"{config['base_url']}"
        headers = config['headers']
        request_data = case['request_data']
        expected = case['expected']

        # 2. 发送请求
        logger.info(f"测试用例 {case['case_id']}: {case['name']}")   
        logger.info(f"请求参数: {request_data}")

        allure.dynamic.title(case['name']) # 动态设置allure报告标题为用例名称
        allure.attach(body=config['base_url'], name='接口地址')  # 添加allure报告显示接口地址
        allure.attach(body=json.dumps(request_data), name='接口参数')  # 添加allure报告显示接口参数

        response = requests.post(url=url, json=request_data, headers=headers)  # 注意json格式入参        
        response_data = response.json()

        logger.info(f"响应结果: {response_data}")
    
        # 3. 断言验证
        try:
            assert response_data['RetCode'] == expected['RetCode'], \
                f"状态码不符，预期: {expected['RetCode']}, 实际: {response_data['RetCode']}"
            assert "ResourceEipDirectModeType" and "SubResourceEipDirectModeType" not in response, \
                f"返回字段不符，预期:{case['name']}响应中不应包含ResourceEipDirectModeType和SubResourceEipDirectModeType字段"            
            logger.info(f"测试用例 {case['case_id']}: {case['name']} 执行通过")
        except AssertionError as e:
            logger.error(f"测试用例 {case['case_id']}: {case['name']} 执行失败: {str(e)}")
            raise

if __name__ == '__main__':
    pytest.main(["-vs", "testcases/test_describe_eip.py"])