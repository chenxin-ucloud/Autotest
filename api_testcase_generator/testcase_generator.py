import json
import re
from typing import List, Dict, Any
from urllib.parse import parse_qs, urlparse
from models import APIInfo, Parameter, TestCase, CaseLevel


class TestCaseGenerator:
    """测试用例生成器 - 从API文档自动生成测试用例"""

    def __init__(self, api_info: APIInfo):
        self.api_info = api_info
        self.base_request = self._parse_request_example()
        self.success_response = self._parse_response_example()
        self.error_response = self._build_error_response()
        self._case_counter = 0

    def _next_case_id(self) -> str:
        self._case_counter += 1
        return f"TC{self._case_counter:03d}"

    def _parse_request_example(self) -> Dict[str, Any]:
        """从请求示例解析基础请求数据 (URL参数格式 &Key=Value)"""
        request_data = {}
        example = self.api_info.request_example
        if not example:
            return request_data

        # 提取所有 Key=Value 对
        pairs = re.findall(r'[&?](\S+?)=(\S+)', example)
        for key, value in pairs:
            request_data[key] = value

        # 根据参数定义进行类型转换
        param_type_map = {p.name: p.param_type for p in self.api_info.request_params}
        for key in list(request_data.keys()):
            # 处理带 .n. 或 .N 后缀的参数名, 查找基础参数名的类型
            base_key = re.sub(r'\.\d+\.', '.n.', key)
            base_key = re.sub(r'\.\d+$', '.n', base_key)
            base_key = re.sub(r'\.N$', '.n', base_key)
            ptype = param_type_map.get(key) or param_type_map.get(base_key)
            if ptype and ptype.lower() == 'int':
                try:
                    request_data[key] = int(request_data[key])
                except (ValueError, TypeError):
                    pass

        return request_data

    def _parse_response_example(self) -> Dict[str, Any]:
        """从响应示例解析成功响应"""
        example = self.api_info.response_example
        if not example:
            return {"RetCode": 0, "Action": f"{self.api_info.action}Response"}
        try:
            return json.loads(example)
        except json.JSONDecodeError:
            return {"RetCode": 0, "Action": f"{self.api_info.action}Response"}

    def _build_error_response(self) -> Dict[str, Any]:
        """构建失败响应 (RetCode=227806)"""
        action_resp = self.success_response.get("Action", f"{self.api_info.action}Response")
        return {"RetCode": 227806, "Action": action_resp}

    def _get_required_params(self) -> List[Parameter]:
        return [p for p in self.api_info.request_params if p.required]

    def _get_optional_params(self) -> List[Parameter]:
        return [p for p in self.api_info.request_params if not p.required]

    def _build_request(self, overrides: Dict[str, Any] = None,
                       remove_keys: List[str] = None) -> Dict[str, Any]:
        """基于基础请求构建修改后的请求数据"""
        data = dict(self.base_request)
        if remove_keys:
            for key in remove_keys:
                # 移除精确匹配的key
                data.pop(key, None)
                # 也移除带数组下标的变体 (如 Resource.0.xxx 对应 Resource.n.xxx)
                pattern = re.sub(r'\.n\.', r'.\\d+.', re.escape(key))
                pattern = re.sub(r'\.n$', r'.\\d+', pattern)
                keys_to_remove = [k for k in data if re.match(pattern, k)]
                for k in keys_to_remove:
                    data.pop(k, None)
        if overrides:
            data.update(overrides)
        return data

    def _find_request_keys_for_param(self, param_name: str) -> List[str]:
        """找到请求数据中与参数定义对应的所有key"""
        keys = []
        if param_name in self.base_request:
            keys.append(param_name)
        # 检查数组形式的key
        pattern = re.sub(r'\.n\.', r'.\\d+.', re.escape(param_name))
        pattern = re.sub(r'\.n$', r'.\\d+', pattern)
        for k in self.base_request:
            if k != param_name and re.match(pattern, k):
                keys.append(k)
        return keys

    def generate(self) -> List[TestCase]:
        """生成所有等级的测试用例"""
        cases = []
        cases.extend(self._generate_p0())
        cases.extend(self._generate_p1())
        cases.extend(self._generate_p2())
        cases.extend(self._generate_p3())
        cases.extend(self._generate_p4())
        return cases

    def _generate_p0(self) -> List[TestCase]:
        """P0 冒烟测试: 全部必填参数正确"""
        request_data = self._build_request()
        return [TestCase(
            case_id=self._next_case_id(),
            case_name=f"{self.api_info.name}-全部参数正确",
            module=f"/{self.api_info.action}",
            precondition="接口服务正常可用",
            steps=f"【1】调用{self.api_info.action}接口\n【2】传入所有必填参数，值合法",
            expected_result=f"【1】返回RetCode=0\n【2】操作成功",
            case_level=CaseLevel.P0,
            tag=self.api_info.action,
            request_data=request_data,
            expected=self.success_response,
        )]

    def _generate_p1(self) -> List[TestCase]:
        """P1 核心功能: 每个必填参数各缺少一个用例"""
        cases = []
        required_params = self._get_required_params()
        for param in required_params:
            keys = self._find_request_keys_for_param(param.name)
            remove_keys = keys if keys else [param.name]
            request_data = self._build_request(remove_keys=remove_keys)
            cases.append(TestCase(
                case_id=self._next_case_id(),
                case_name=f"{self.api_info.name}-缺少必填参数{param.name}",
                module=f"/{self.api_info.action}",
                precondition="接口服务正常可用",
                steps=f"【1】调用{self.api_info.action}接口\n【2】不传入必填参数{param.name}",
                expected_result=f"【1】返回错误码\n【2】提示缺少必填参数{param.name}",
                case_level=CaseLevel.P1,
                tag=self.api_info.action,
                request_data=request_data,
                expected=self.error_response,
            ))
        return cases

    def _generate_p2(self) -> List[TestCase]:
        """P2 重要功能: 必填参数类型错误"""
        cases = []
        required_params = self._get_required_params()
        for param in required_params:
            if param.param_type.lower() == 'int':
                # int传string
                keys = self._find_request_keys_for_param(param.name)
                override_key = keys[0] if keys else param.name
                request_data = self._build_request(overrides={override_key: "invalid_string"})
                cases.append(TestCase(
                    case_id=self._next_case_id(),
                    case_name=f"{self.api_info.name}-{param.name}传入字符串",
                    module=f"/{self.api_info.action}",
                    precondition="接口服务正常可用",
                    steps=f"【1】调用{self.api_info.action}接口\n【2】参数{param.name}传入字符串类型",
                    expected_result=f"【1】返回错误码\n【2】提示参数{param.name}类型错误",
                    case_level=CaseLevel.P2,
                    tag=self.api_info.action,
                    request_data=request_data,
                    expected=self.error_response,
                ))
            elif param.param_type.lower() == 'string':
                # string传int
                keys = self._find_request_keys_for_param(param.name)
                override_key = keys[0] if keys else param.name
                request_data = self._build_request(overrides={override_key: 12345})
                cases.append(TestCase(
                    case_id=self._next_case_id(),
                    case_name=f"{self.api_info.name}-{param.name}传入整数",
                    module=f"/{self.api_info.action}",
                    precondition="接口服务正常可用",
                    steps=f"【1】调用{self.api_info.action}接口\n【2】参数{param.name}传入整数类型",
                    expected_result=f"【1】返回错误码\n【2】提示参数{param.name}类型错误",
                    case_level=CaseLevel.P2,
                    tag=self.api_info.action,
                    request_data=request_data,
                    expected=self.error_response,
                ))
        return cases

    def _generate_p3(self) -> List[TestCase]:
        """P3 一般功能: 各可选参数传入合法值"""
        cases = []
        optional_params = self._get_optional_params()
        for param in optional_params:
            # 跳过数组下标变体参数 (如 ResourceLabel.n.Key)
            if '.n.' in param.name:
                continue
            keys = self._find_request_keys_for_param(param.name)
            if keys:
                # 参数已在基础请求中, 确保其值合法
                request_data = self._build_request()
            else:
                # 参数不在基础请求中, 生成合法值并加入
                if param.param_type.lower() == 'int':
                    override = {param.name: 1}
                else:
                    override = {param.name: "test_value"}
                request_data = self._build_request(overrides=override)
            cases.append(TestCase(
                case_id=self._next_case_id(),
                case_name=f"{self.api_info.name}-传入可选参数{param.name}",
                module=f"/{self.api_info.action}",
                precondition="接口服务正常可用",
                steps=f"【1】调用{self.api_info.action}接口\n【2】传入可选参数{param.name}，值合法",
                expected_result=f"【1】返回RetCode=0\n【2】操作成功",
                case_level=CaseLevel.P3,
                tag=self.api_info.action,
                request_data=request_data,
                expected=self.success_response,
            ))
        return cases

    def _generate_p4(self) -> List[TestCase]:
        """P4 边界测试: int传0/负数, string传空串/超长串"""
        cases = []
        all_params = self.api_info.request_params
        for param in all_params:
            # 跳过数组下标变体参数
            if '.n.' in param.name:
                continue
            keys = self._find_request_keys_for_param(param.name)
            override_key = keys[0] if keys else param.name

            if param.param_type.lower() == 'int':
                # int传0
                request_data = self._build_request(overrides={override_key: 0})
                cases.append(TestCase(
                    case_id=self._next_case_id(),
                    case_name=f"{self.api_info.name}-{param.name}为0",
                    module=f"/{self.api_info.action}",
                    precondition="接口服务正常可用",
                    steps=f"【1】调用{self.api_info.action}接口\n【2】参数{param.name}传入0",
                    expected_result=f"【1】返回错误码\n【2】提示参数{param.name}边界值异常",
                    case_level=CaseLevel.P4,
                    tag=self.api_info.action,
                    request_data=request_data,
                    expected=self.error_response,
                ))
                # int传负数
                request_data = self._build_request(overrides={override_key: -1})
                cases.append(TestCase(
                    case_id=self._next_case_id(),
                    case_name=f"{self.api_info.name}-{param.name}为负数",
                    module=f"/{self.api_info.action}",
                    precondition="接口服务正常可用",
                    steps=f"【1】调用{self.api_info.action}接口\n【2】参数{param.name}传入-1",
                    expected_result=f"【1】返回错误码\n【2】提示参数{param.name}边界值异常",
                    case_level=CaseLevel.P4,
                    tag=self.api_info.action,
                    request_data=request_data,
                    expected=self.error_response,
                ))
            elif param.param_type.lower() == 'string':
                # string传空串
                request_data = self._build_request(overrides={override_key: ""})
                cases.append(TestCase(
                    case_id=self._next_case_id(),
                    case_name=f"{self.api_info.name}-{param.name}为空字符串",
                    module=f"/{self.api_info.action}",
                    precondition="接口服务正常可用",
                    steps=f"【1】调用{self.api_info.action}接口\n【2】参数{param.name}传入空字符串",
                    expected_result=f"【1】返回错误码\n【2】提示参数{param.name}不能为空",
                    case_level=CaseLevel.P4,
                    tag=self.api_info.action,
                    request_data=request_data,
                    expected=self.error_response,
                ))
                # string传超长串
                long_str = "A" * 256
                request_data = self._build_request(overrides={override_key: long_str})
                cases.append(TestCase(
                    case_id=self._next_case_id(),
                    case_name=f"{self.api_info.name}-{param.name}超长字符串",
                    module=f"/{self.api_info.action}",
                    precondition="接口服务正常可用",
                    steps=f"【1】调用{self.api_info.action}接口\n【2】参数{param.name}传入256位超长字符串",
                    expected_result=f"【1】返回错误码\n【2】提示参数{param.name}长度超限",
                    case_level=CaseLevel.P4,
                    tag=self.api_info.action,
                    request_data=request_data,
                    expected=self.error_response,
                ))
        return cases
