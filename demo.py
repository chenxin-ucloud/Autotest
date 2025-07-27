import requests
import uuid

def generate_request_uuid():
    """生成请求UUID的函数"""
    return f"{str(uuid.uuid4()).replace('-', '')[:20]}-{str(uuid.uuid4()).replace('-', '')[:4]}"

def make_api_request(request_uuid):
    """使用生成的UUID发起API请求"""
    url = "http://internal-api-test03.service.ucloud.cn"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "Action": "DescribeEIP",
        "az_group": 666006,
        "EIPIds.0": "eip-1emm2ltcp5vm",
        "Backend": "unetfe-internal",
        "top_organization_id": 1380002,
        "organization_id": 1560006,
        "channel": 1,
        "Limit": 300,
        "request_uuid": request_uuid
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 生成UUID
    request_uuid = generate_request_uuid()
    print(f"生成的请求UUID: {request_uuid}")
    
    # 发起请求
    result = make_api_request(request_uuid)
    if result:
        print("API响应:", result)