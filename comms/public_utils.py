import uuid
import json
import hashlib
from typing import Dict, Any


# 生成请求UUID，格式如: 7937bcfc-c99c-438b-ace7-9dd3f0ebdb3c
def generate_request_uuid() -> str:       
    return str(uuid.uuid4())

