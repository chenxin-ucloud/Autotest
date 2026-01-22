# API配置文件 - 集中管理所有API接口配置
import hashlib
from typing import Dict, Any

# 公私钥配置
AUTH_CONFIG = {
    "public_key": "4Dx4L5XtI4tAL3JxycJn0U4HpVVoUavw",  # 请替换为实际的PublicKey
    "private_key": "6UIzd9LEs7K4JSASke3bTAJMl5b6zpBiZ3Fraqah6Ane"  # 请替换为实际的PrivateKey
}
# 通用的API基础配置
API_CONFIG = {   
        "base_url": "http://api-test03.ucloudadmin.com",
        "method": "POST",
        "timeout": 10    
}
# 共用的请求头配置
COMMON_HEADERS = {
    "Content-Type": "application/json",
    "Cookie": "is_dark_theme_on=0; channel_key=; s_t=0; d_i=a7b93f15-84d1-498f-ad82-b3cb06880e7b; _gcl_au=1.1.626339893.1765780587; _ga=GA1.2.298412183.1730883104; _ga_WTG413V9QJ=GS2.1.s1766628896$o108$g0$t1766628900$j56$l0$h0; logged_out_marketing_header_id=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqVTNOamt5TWprekxXWXlabVV0TkdVeE1DMWhNRE5pTFRObU16ZGpPV1EzTmpFME1DST0iLCJleHAiOm51bGwsInB1ciI6ImNvb2tpZS5sb2dnZWRfb3V0X21hcmtldGluZ19oZWFkZXJfaWQifX0%3D--c5b2f8dd856f50840ab36a55ad8e2309276bb0f1; Hm_lvt_c9dae94ecdf19556360bd26cffbb9e20=1766367661,1766973244,1767492037,1768181626; INNER_AUTH_TOKEN=FmiivYkVzIkOMXsNs14R6RqXZ5/CLzzotH8OQ5IJYNRbUpjXZh0tbldC2JjvqNe4WJW/uM5eQ1GrVXricP4GWw==; _uetsid=21641800f5cf11f0ba4a733768e6a9dc|48wvhy|2|g2v|0|2211; _uetvid=76e80bc0bc5211efb9d4311eb732a18c|1taxx5a|1768893042583|1|1|bat.bing.com/p/conversions/c/v; U_USER_EMAIL=xin.chen%40ucloud.cn; U_COMPANY_ID=1620004; U_USER_ID=1710009; U_MANAGER=; U_JWT_TOKEN=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Njk0OTc4NDcsImp0aSI6Ikc0OUVOdWhWcDluRXZ0Z1d5SVYyMWYiLCJpYXQiOjE3Njg4OTMwNDcsInN1YiI6InVjczppYW06OjE2MjAwMDQ6dXNlci8xNzEwMDA5Iiwicm9vdCI6dHJ1ZSwic2QiOnt9fQ.znvMBKPSbDPLzRuGKBwD4wPC0W8Fqynds4VtAVSIKXC4kY22Lh-7I8cO5STP8E6-YAOPWocSYmnl6tMvm411ug; U_CSRF_TOKEN=cac59c03e68980fc8441eb46f3d30d53; U_CHANNEL_ID=666; c_project_xin_chen_ucloud_cn={%22ProjectId%22:%22org-4fqheo%22%2C%22ProjectName%22:%22Autotest-1620009%22}; c_last_region_xin_chen_ucloud_cn={%22Region%22:%22test05%22%2C%22Zone%22:%22test05-01%22}; c_region_xin_chen_ucloud_cn={%22Region%22:%22test05%22%2C%22Zone%22:%22$%22}"
}

def generate_signature(params: Dict[str, Any]) -> str:
    """
    生成UCloud API签名
    
    Args:
        params: 请求参数字典
    
    Returns:
        生成的签名字符串
    """
    public_key = AUTH_CONFIG['public_key']
    private_key = AUTH_CONFIG['private_key']
    
    # 将params转为副本，避免修改原始参数
    params_copy = params.copy()
    
    # 添加PublicKey到参数中
    params_copy['PublicKey'] = public_key
    
    # 对参数按键排序，并生成签名字符串
    sorted_keys = sorted(params_copy.keys())
    sign_str = ''.join([
        f'{key}{params_copy[key]}' 
        for key in sorted_keys 
        if key != 'Signature'
    ])
    
    # 添加PrivateKey到签名字符串后面
    sign_str += private_key
    
    # 使用SHA1计算签名
    signature = hashlib.sha1(sign_str.encode()).hexdigest()
    
    return signature


def prepare_request_body(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    为请求准备body，自动添加PublicKey和Signature
    
    Args:
        params: 原始请求参数字典
    
    Returns:
        包含PublicKey和Signature的完整请求体
    """
    request_body = params.copy()
    
    # 生成签名
    signature = generate_signature(params)
    
    # 添加PublicKey和Signature到请求体
    request_body['PublicKey'] = AUTH_CONFIG['public_key']
    request_body['Signature'] = signature
    
    return request_body
