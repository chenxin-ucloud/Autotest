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

def run_tests(test_type="all"):
    """运行测试"""
    reports_dir = create_reports_dir()
    
    # 生成带时间戳的报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = os.path.join(reports_dir, f"report_{timestamp}.html")
    json_report = os.path.join(reports_dir, f"report_{timestamp}.json")
    
    # 构建pytest命令
    cmd = [
        "pytest",
        "-v",
        "--tb=short",
        f"--html={html_report}",
        f"--json={json_report}",
        "--self-contained-html"
    ]
    
    # 根据测试类型添加参数
    if test_type == "normal":
        cmd.extend(["-k", "test_describe_eip_normal_scenarios"])
    elif test_type == "error":
        cmd.extend(["-k", "test_describe_eip_error_scenarios"])
    elif test_type == "performance":
        cmd.extend(["-k", "test_describe_eip_performance"])
    elif test_type == "all":
        cmd.append("test_describe_eip.py")
    else:
        print(f"未知的测试类型: {test_type}")
        return False
    
    print(f"运行测试命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("测试执行成功!")
        print(f"HTML报告: {html_report}")
        print(f"JSON报告: {json_report}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"测试执行失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

if __name__ == "__main__":
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    success = run_tests(test_type)
    sys.exit(0 if success else 1) 