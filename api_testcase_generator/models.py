from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class CaseLevel(Enum):
    """用例等级"""
    P0 = "P0-冒烟测试"
    P1 = "P1-核心功能"
    P2 = "P2-重要功能"
    P3 = "P3-一般功能"
    P4 = "P4-边界测试"


@dataclass
class Parameter:
    """接口参数"""
    name: str
    param_type: str
    description: str
    required: bool


@dataclass
class APIInfo:
    """接口信息"""
    name: str                           # 接口名称
    action: str                         # 操作名称
    description: str                    # 接口描述
    request_params: List[Parameter] = field(default_factory=list)
    response_params: List[Parameter] = field(default_factory=list)
    request_example: str = ""
    response_example: str = ""


@dataclass
class TestCase:
    """测试用例"""
    case_id: str                        # 用例ID
    case_name: str                      # 用例名称
    module: str                         # 所属模块
    precondition: str                   # 前置条件
    steps: str                          # 步骤描述
    expected_result: str                # 预期结果
    case_level: CaseLevel               # 用例等级
    tag: str = ""                       # 标签 (模板C列)
    remark: str = ""                    # 备注 (模板E列)
    case_type: int = 1                  # 用例类型 (模板I列, 1=功能)
    support_automation: int = 1         # 是否支持自动化 (模板J列)
    support_polling: int = 1            # 是否支持拨测 (模板K列)
    request_data: dict = field(default_factory=dict)   # 请求数据 (JSON输出用)
    expected: dict = field(default_factory=dict)        # 期望响应 (JSON输出用)

    def to_dict(self) -> dict:
        return {
            "用例ID": self.case_id,
            "用例名称": self.case_name,
            "所属模块": self.module,
            "前置条件": self.precondition,
            "步骤描述": self.steps,
            "预期结果": self.expected_result,
            "用例等级": self.case_level.value
        }

    def to_excel_row(self) -> list:
        """返回模板11列对应的值列表"""
        # 用例等级只取 P0/P1 等前缀
        level_prefix = self.case_level.value.split("-")[0] if "-" in self.case_level.value else self.case_level.value
        return [
            self.case_name,             # A: 用例名称
            self.module,                # B: 所属模块
            self.tag,                   # C: 标签
            self.precondition,          # D: 前置条件
            self.remark,                # E: 备注
            self.steps,                 # F: 步骤描述
            self.expected_result,       # G: 预期结果
            level_prefix,               # H: 用例等级
            self.case_type,             # I: 用例类型
            self.support_automation,    # J: 是否支持自动化
            self.support_polling,       # K: 是否支持拨测
        ]

    def to_framework_dict(self) -> dict:
        """返回测试框架格式字典"""
        return {
            "case_id": self.case_id,
            "name": self.case_name,
            "request_data": self.request_data,
            "expected": self.expected,
        }
