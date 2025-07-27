import pytest
import requests
import yaml
import os

class TestDescribeEIP:
    # 读取YAML测试数据
    @pytest.fixture(scope="class")
    def test_data(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, "test_describe_eip.yml")
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["test_cases"]

    # 参数化执行所有测试用例
    @pytest.mark.parametrize("case", [])
    def test_describe_eip(self, case):
        # 1. 发送请求
        url = case["request"]["url"]
        headers = case["request"]["headers"]
        request_data = case["request"]["data"]
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=request_data,
                timeout=10
            )
            response_json = response.json()
        except Exception as e:
            pytest.fail(f"请求发送失败: {str(e)}")

        # 2. 基础响应断言（状态码、Action）
        assert response.status_code == 200, "HTTP响应状态码非200"
        assert response_json.get("RetCode") == case["expected"]["RetCode"], \
            f"RetCode断言失败，实际: {response_json.get('RetCode')}"
        assert response_json.get("Action") == case["expected"]["Action"], \
            f"Action断言失败，实际: {response_json.get('Action')}"

        # 3. EIPSet详细断言
        expected_eip_set = case["expected"].get("EIPSet", [])
        actual_eip_set = response_json.get("EIPSet", [])
        assert len(actual_eip_set) >= 1, "EIPSet为空，未查询到EIP信息"

        # 匹配当前测试用例的EIP数据
        target_eip_id = expected_eip_set[0]["EIPId"]
        matched_eip = next(
            (eip for eip in actual_eip_set if eip.get("EIPId") == target_eip_id),
            None
        )
        assert matched_eip is not None, f"未找到EIPId: {target_eip_id}的记录"       

    # 在类中使用fixture来设置参数化的值
    @pytest.fixture(autouse=True)
    def set_parametrize_values(self, request, test_data):
        marker = request.node.get_closest_marker("parametrize")
        if marker and marker.args[0] == "case":
            new_marker = pytest.mark.parametrize("case", test_data)
            request.node.add_marker(new_marker)

if __name__ == "__main__":
    pytest.main(["-v", "test_describe_eip.py", "--html=report.html"])