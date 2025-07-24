# IPv6 网关接口自动化测试

本项目基于 Pytest + Requests + YAML 实现 IPv6 网关及相关带宽接口的自动化测试。

## 目录结构

- `test_api.py`：主测试用例文件，自动读取 YAML 测试数据并执行接口测试
- `test_data.yml`：接口测试数据，包含各接口的请求参数与预期返回
- `api_document.md`：接口文档，详细描述了所有接口的参数和返回结构
- `README.md`：项目说明文档

## 环境依赖

- Python 3.6+
- pytest
- requests
- pyyaml

安装依赖：

```sh
pip install pytest requests pyyaml
```

## 使用方法

1. 修改 `test_api.py` 中的 `url` 变量为实际的 API 地址。
2. 根据需要完善 `test_api.py`，为每个接口添加对应的测试方法（如 `test_delete_ipv6_gateway`、`test_modify_ipv6_gateway` 等）。
3. 运行测试：

```sh
pytest test_api.py
```

## 测试数据说明

所有测试数据均存放于 [`test_data.yml`](test_data.yml)，每个接口下包含多个测试用例，结构如下：

```yml
CreateIpv6Gateway:
  - name: 创建 IPv6 网关成功
    request:
      Action: CreateIpv6Gateway
      ...
    expected:
      Action: CreateIpv6GatewayResponse
      RetCode: 0
      ...
```

## 扩展说明

- 可根据 [`api_document.md`](api_document.md) 补充更多接口的测试用例和断言逻辑。
- 支持自定义断言、异常处理和日志输出。

## 参考

- [pytest 官方文档](https://docs.pytest.org/)
- [requests 官方文档](https://docs.python-requests.org/)
- [PyYAML 官方文档](https://pyyaml.org/wiki/PyYAMLDocumentation)