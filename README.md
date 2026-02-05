# Autotest 自动化测试框架

基于 **pytest** 的接口自动化测试框架，支持 JSON/YAML 测试数据、Allure 报告、统一日志与 UCloud API 签名。

## 技术栈

- **pytest** ≥ 7.0 — 测试框架
- **requests** ≥ 2.28 — HTTP 请求
- **allure-pytest** ≥ 2.9.45 — Allure 测试报告
- **PyYAML** ≥ 6.0 — YAML 配置与数据

## 项目结构

```
Autotest/
├── comms/                 # 公共模块
│   ├── constants.py       # 路径与常量（项目根、用例目录、数据目录、日志、报告）
│   ├── config.py          # API 配置（base_url、鉴权、签名，需自行维护，不纳入版本库）
│   ├── json_utils.py      # JSON 数据加载与测试用例提取
│   ├── yaml_utils.py      # YAML 数据加载与测试用例提取
│   ├── log_utils.py       # 日志配置（控制台 + info.log / error.log）
│   └── public_utils.py    # 通用工具（如 UUID 生成）
├── testcases/             # 测试用例（test_*.py）
├── datas/                 # 测试数据（JSON/YAML）
├── logs/                  # 日志输出
├── reports/               # 测试报告（如 Allure）
├── pytest.ini              # pytest 配置
├── requirements.txt       # 依赖
└── README.md
```

## 环境准备

### 1. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. API 配置

项目中的 `comms/config.py` 未纳入版本库，需在本地自行创建或从模板复制，包含：

- `AUTH_CONFIG`：公私钥等鉴权信息
- `API_CONFIG`：如 `base_url`、`method`、`timeout`
- `COMMON_HEADERS`：公共请求头（如 Cookie）
- `generate_signature()` / `prepare_request_body()`：UCloud API 签名与请求体封装

请勿将含敏感信息的 `config.py` 提交到仓库。

## 运行测试

- 运行全部用例（用例目录由 `pytest.ini` 指定为 `./testcases`）：

```bash
pytest
```

- 指定文件或目录：

```bash
pytest testcases/
pytest testcases/test_list_nta_enum.py
```

- 生成 Allure 结果并查看报告：

```bash
pytest --alluredir=reports/allure_json
allure serve reports/allure_json
```

- 常用参数示例：

```bash
pytest -v                    # 详细输出
pytest -s                    # 显示 print
pytest -k "关键字"            # 按名称过滤用例
```

## 用例与数据约定

- **用例脚本**：放在 `testcases/` 下，文件名以 `test_` 开头，类名以 `Test` 开头，方法名以 `test_` 开头（与 `pytest.ini` 一致）。
- **测试数据**：放在 `datas/` 下，可由 `comms.json_utils.JsonDataLoader` 或 `comms.yaml_utils.YamlDataLoader` 加载；若数据结构中包含 `test_cases` 列表，可使用对应的 `get_test_cases()` 获取用例数据。

## 日志与报告

- **日志**：通过 `comms.log_utils.logger` 输出；INFO 及以上写入控制台与 `logs/info.log`，ERROR 写入 `logs/error.log`。
- **报告**：默认使用 Allure，结果目录为 `reports/allure_json`，可用 `allure serve` 或 `allure generate` 生成 HTML。

## 注意事项

- `datas/`、`testcases/`、`comms/config.py`、`logs/`、`reports/` 等已在 `.gitignore` 中忽略，请在本机维护测试数据与配置。
- 首次使用前请确认已正确配置 `comms/config.py` 及 Allure 命令行环境（如已安装 Allure 并加入 PATH）。
