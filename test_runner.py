# encoding=utf-8
import pytest
import os
from comms.constants import REPORT_JSON, REPORT_HTML, CASE_DIR

"""
使用allure生成测试报告
    1.https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/  官网下载allure的zip压缩包
    2.解压到tools目录下,如: D:/tools/allure-2.17.0
    3.添加allure的bin目录到环境变量path中
    4.在cmd中命令行输入allure --version 回车,验证是否安装成功
    5.在cmd命令行输入pip install allure-pytest 安装pytest框架的allure插件
"""

if __name__ == '__main__':
    pytest.main(["--alluredir", REPORT_JSON, '--clean-alluredir', CASE_DIR])
    os.system('allure generate %s -o %s --clean' % (REPORT_JSON, REPORT_HTML))
