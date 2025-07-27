# 测试配置文件
import os
from typing import Dict, Any

class TestConfig:
    """测试配置类"""
    
    # 基础配置
    BASE_URL = "http://internal-api-test03.service.ucloud.cn"
    TIMEOUT = 10
    DEFAULT_HEADERS = {
        "Content-Type": "application/json"
    }
    
    # 测试环境配置
    AZ_GROUP = 666006
    TOP_ORGANIZATION_ID = 1380002
    ORGANIZATION_ID = 1560006
    CHANNEL = 1
    BACKEND = "unetfe-internal"
    
    # 报告配置
    REPORT_DIR = "reports"
    HTML_REPORT = "report.html"
    JSON_REPORT = "report.json"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def get_request_headers(cls) -> Dict[str, str]:
        """获取请求头"""
        return cls.DEFAULT_HEADERS.copy()
    
    @classmethod
    def get_base_params(cls) -> Dict[str, Any]:
        """获取基础请求参数"""
        return {
            "az_group": cls.AZ_GROUP,
            "Backend": cls.BACKEND,
            "top_organization_id": cls.TOP_ORGANIZATION_ID,
            "organization_id": cls.ORGANIZATION_ID,
            "channel": cls.CHANNEL
        } 