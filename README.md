# DescribeEIP接口自动化测试框架

基于pytest的DescribeEIP接口自动化测试框架，使用YAML文件管理测试数据，实现数据和测试脚本分离。

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **验证框架**
   ```bash
   python test_framework_validation.py
   ```

3. **运行测试**
   ```bash
   python run_tests.py
   ```

4. **查看报告**
   测试完成后，在 `reports/` 目录下查看HTML和JSON格式的测试报告。

## 项目结构

```
Autotest_New/
├── config.py                    # 配置文件
├── utils.py                     # 工具类
├── test_describe_eip.py         # 测试脚本
├── test_describe_eip.yml        # 测试数据
├── test_framework_validation.py # 框架验证脚本
├── pytest.ini                  # pytest配置
├── requirements.txt             # 依赖包
├── run_tests.py                # 测试运行脚本
├── reports/                    # 测试报告目录
├── DescribeEIP.md              # 接口文档
└── README.md                   # 项目说明
```

## 环境依赖

- Python 3.6+
- pytest
- requests
- pyyaml
- pytest-html
- pytest-json-report

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 运行所有测试
```bash
python run_tests.py
# 或者
pytest test_describe_eip.py -v
```

### 2. 运行特定类型测试
```bash
# 运行正常场景测试
python run_tests.py normal

# 运行异常场景测试
python run_tests.py error

# 运行性能测试
python run_tests.py performance
```

### 3. 生成HTML报告
```bash
pytest test_describe_eip.py --html=reports/report.html --self-contained-html
```

## 测试数据管理

测试数据存储在`test_describe_eip.yml`文件中，包含：

- **配置信息**: 基础URL、超时时间、请求头等
- **测试用例**: 正常场景、异常场景、边界条件等
- **测试数据**: 有效的EIP ID、IP地址等

### 添加新测试用例

在YAML文件中添加新的测试用例：

```yaml
- case_id: "TC007"
  name: "新测试用例名称"
  description: "测试用例描述"
  request:
    method: "POST"
    data:
      Action: "DescribeEIP"
      # 其他请求参数
  expected:
    RetCode: 0
    Action: "DescribeEIPResponse"
    # 其他期望结果
```

## 测试报告

测试完成后，会在`reports`目录下生成：

- `report_YYYYMMDD_HHMMSS.html`: HTML格式测试报告
- `report_YYYYMMDD_HHMMSS.json`: JSON格式测试报告

## 配置说明

### 环境配置

在`config.py`中修改测试环境配置：

```python
class TestConfig:
    BASE_URL = "http://your-api-url"
    AZ_GROUP = 666006
    TOP_ORGANIZATION_ID = 1380002
    # 其他配置...
```

### 测试数据配置

在`test_describe_eip.yml`中修改测试数据：

```yaml
config:
  base_url: "http://your-api-url"
  timeout: 10
  headers:
    Content-Type: "application/json"
```

## 扩展功能

### 1. 添加新的断言方法

在`utils.py`中添加新的验证方法：

```python
@staticmethod
def validate_custom_field(response, field_name, expected_value):
    """自定义字段验证"""
    actual_value = response.get(field_name)
    assert actual_value == expected_value, f"{field_name}验证失败"
```

### 2. 添加新的测试场景

在测试类中添加新的测试方法：

```python
def test_new_scenario(self, test_data, config):
    """新测试场景"""
    # 测试逻辑
    pass
```

## 注意事项

1. 确保测试环境网络连接正常
2. 测试数据中的EIP ID需要是有效的
3. 大量测试时注意API调用频率限制
4. 定期更新测试数据以保持测试的有效性

## 故障排除

### 常见问题

1. **导入错误**: 确保所有依赖包已正确安装
2. **网络超时**: 检查网络连接和API服务状态
3. **数据验证失败**: 检查测试数据是否与实际环境匹配

### 调试模式

启用详细日志输出：

```bash
pytest test_describe_eip.py -v -s --log-cli-level=DEBUG
```

### 框架验证

运行框架验证测试，确保所有组件正常工作：

```bash
python test_framework_validation.py
```

这将验证：
- 配置文件加载
- 工具函数功能
- YAML数据结构
- 测试数据内容
- 项目文件结构

## 接口文档

详细的接口文档请参考 [DescribeEIP.md](DescribeEIP.md)

## 参考

- [pytest 官方文档](https://docs.pytest.org/)
- [requests 官方文档](https://docs.python-requests.org/)
- [PyYAML 官方文档](https://pyyaml.org/wiki/PyYAMLDocumentation)