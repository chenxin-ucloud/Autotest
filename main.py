# main.py - 自动化测试总入口，执行 testcases 目录下所有用例

import sys
import pytest

from comms.constants import CASE_DIR


def run_all_tests():
    """执行 testcases 目录下所有测试脚本。"""
    args = [
        CASE_DIR,
        '--report=report.html',
        '--title=测试报告',
        '--tester=测试员',
        '--desc=报告描述信息',
        '--template=1',
    ]
    return pytest.main(args)


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)