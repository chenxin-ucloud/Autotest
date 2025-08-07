"""
使用常量对路径进行管理
好处：可移植性高，通过获取当前文件的目录来定位路径
"""
import os

# 获取项目路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 测试用例执行文件所在路径
CASE_DIR = os.path.join(BASE_DIR, 'testcases')

# 测试数据所在路径
DATA_DIR = os.path.join(BASE_DIR, "datas")
DATA_FILE = os.path.join(DATA_DIR, "describe_eip.json")

# log所在路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')
INFO_FILE = os.path.join(LOG_DIR, 'info.log')
ERROR_FILE = os.path.join(LOG_DIR, 'error.log')

# 测试报告所在路径
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
REPORT_JSON = os.path.join(REPORT_DIR, 'allure_json')
REPORT_HTML = os.path.join(REPORT_DIR, 'allure_html')