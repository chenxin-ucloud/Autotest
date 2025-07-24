import pytest
import requests
import yaml

# 读取 YAML 文件
with open('test_data.yml', 'r', encoding='utf-8') as f:
    test_data = yaml.safe_load(f)

# 定义测试类
class TestAPIs:
    @pytest.mark.parametrize("case", test_data.get('CreateIpv6Gateway', []))
    def test_create_ipv6_gateway(self, case):
        url = "your_api_url"  # 替换为实际的 API 地址
        response = requests.post(url, json=case['request'])
        res = response.json()
        try:
            for key, value in case['expected'].items():
                assert res.get(key) == value
        except AssertionError as e:
            print(f"测试用例 {case['name']} 执行失败！实际结果是 {res}")
            raise e
        else:
            print(f"测试用例 {case['name']} 执行成功！")

    # 为其他接口添加类似的测试方法，如 test_delete_ipv6_gateway、test_modify_ipv6_gateway 等