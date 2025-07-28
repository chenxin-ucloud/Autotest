#!/usr/bin/env python3
"""
测试运行脚本
"""
import os
import sys
import subprocess
from datetime import datetime

def create_reports_dir():
    """创建报告目录"""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return reports_dir

def run_tests():
    """运行全部测试"""
    reports_dir = create_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = os.path.join(reports_dir, f"report_{timestamp}.html")
    cmd = [
        "pytest",
        "-v",
        "--tb=short",
        f"--html={html_report}",
        "--self-contained-html",
        "test_describe_eip.py"
    ]
    print(f"运行测试命令: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("测试执行成功!")
        print(f"HTML报告: {html_report}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"测试执行失败: {e}")
        # 说明：e.stderr 可能为空，因为pytest大部分输出都在stdout
        print(f"错误输出(stderr): {e.stderr}")
        print(f"标准输出(stdout): {e.stdout}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 