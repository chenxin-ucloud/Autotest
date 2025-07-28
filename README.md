# DescribeEIP接口自动化测试框架

基于pytest的DescribeEIP接口自动化测试框架，测试数据与脚本分离，数据采用JSON文件管理。

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行全部测试**
   ```bash
   python run_tests.py
   # 或者
   pytest test_describe_eip.py -v
   ```

3. **查看报告**
   测试完成后，在 `reports/` 目录下查看HTML格式的测试报告。

## 项目结构

```
Autotest_New/
├── config.py                  # 配置文件
├── utils.py                   # 工具类
├── test_describe_eip.py       # 测试脚本
├── test_describe_eip.json     # 测试数据（JSON格式）
├── pytest.ini                 # pytest配置
├── requirements.txt           # 依赖包
├── run_tests.py               # 测试运行脚本
├── reports/                   # 测试报告目录
├── DescribeEIP.md             # 接口文档
└── README.md                  # 项目说明
```

## 环境依赖

- Python 3.6+
- pytest
- requests
- pyyaml
- pytest-html

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 运行全部测试
```bash
python run_tests.py
# 或
pytest test_describe_eip.py -v
```

### 2. 生成HTML报告
```bash
pytest test_describe_eip.py --html=reports/report.html --self-contained-html
```

## 测试数据管理

测试数据存储在`test_describe_eip.json`文件中，包括：
- **配置信息**: 基础URL、超时时间、请求头等
- **测试用例**: 正常场景、异常场景、边界条件等

### 添加新测试用例

在JSON文件中添加新的测试用例对象即可。例如：
```json
{
  "case_id": "TC002",
  "name": "新测试用例名称",
  "description": "测试用例描述",
  "request": {
    "method": "POST",
    "data": { "Action": "DescribeEIPWithAllNum" }
  },
  "expected": {
    "RetCode": 0,
    "Action": "DescribeEIPWithAllNumResponse"
  }
}
```

## 测试报告

测试完成后，会在`reports`目录下生成：
- `report_YYYYMMDD_HHMMSS.html`: HTML格式测试报告

## 配置说明

### 环境配置

在`config.py`中可修改测试环境配置：
```python
class TestConfig:
    BASE_URL = "http://your-api-url"
    # 其他配置...
```

### 测试数据配置

在`test_describe_eip.json`中修改测试数据：
```json
"config": {
  "base_url": "http://your-api-url",
  "timeout": 10,
  "headers": { "Content-Type": "application/json" }
}
```

## 注意事项

1. 确保测试环境网络连接正常
2. 测试数据中的EIP ID需为有效值
3. 大量测试时注意API调用频率限制
4. 定期更新测试数据以保持测试的有效性

## 故障排除

1. **依赖导入错误**: 确保所有依赖包已正确安装
2. **网络超时**: 检查网络连接和API服务状态
3. **数据验证失败**: 检查测试数据是否与实际环境匹配

## 接口文档

详细接口文档请参考 [DescribeEIP.md](DescribeEIP.md)

## 参考
- [pytest 官方文档](https://docs.pytest.org/)
- [requests 官方文档](https://docs.python-requests.org/)
- [PyYAML 官方文档](https://pyyaml.org/wiki/PyYAMLDocumentation)