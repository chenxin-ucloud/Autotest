# DescribeEIP 接口自动化测试框架

本项目基于 Pytest + Allure，采用数据驱动方式实现 DescribeEIP 接口自动化测试。测试数据与用例分离，支持 JSON/YAML 格式，自动生成测试报告。

## 目录结构

```
Autotest/
├── comms/           # 工具模块（常量、日志、数据加载等）
├── datas/           # 测试数据（JSON/YAML）
├── logs/            # 日志输出目录
├── reports/         # 测试报告目录
├── testcases/       # 测试用例
├── test_runner.py   # 主运行入口
├── pytest.ini       # Pytest 配置
├── requirements.txt # 依赖包
└── README.md        # 项目说明
```

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行全部测试并生成 Allure 报告**
   ```bash
   python test_runner.py
   ```
   ***或手动运行单个用例***
   ```bash
   python -m testcases.test_describe_eip
   ```

3. **查看报告**
   - 启动本地服务： 
   ```bash
   allure serve reports/allure_json
   ```
   ***或者***
   ```bash
   allure open reports/allure_html
   ```

## 测试用例开发

- 用例统一放在 `testcases/` 目录，支持类/函数式风格。
- 测试数据存放于 `datas/` 目录，支持 JSON/YAML 格式。
- 用例通过 `comms/json_utils.py` 或自定义工具加载数据，参数化执行。

## 日志与报告

- 日志输出至 `logs/` 目录，分 info.log 和 error.log。
- 测试报告输出至 `reports/` 目录，支持 Allure 可视化。

## 依赖说明

- Python 3.6+
- pytest
- requests
- allure-pytest
- pyyaml（如需支持 YAML 数据）

## 注意事项

- 确保 Allure 命令行工具已安装并配置环境变量（详见 test_runner.py 注释）。
- 测试数据需与实际接口参数保持同步。
- 大量测试时注意 API 调用频率限制。

## 参考

- [pytest 官方文档](https://docs.pytest.org/)
- [requests 官方文档](https://docs.python-requests.org/)
- [Allure 官方文档](https://docs.qameta.io/allure/)
- [PyYAML 官方文档](https://pyyaml.org/wiki/PyYAMLDocumentation)