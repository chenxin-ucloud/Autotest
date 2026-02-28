# 创建流量分析任务 接口测试用例

> 生成时间: 2026-02-13 13:53:48
> 接口名称: CreateNTATask

## 用例列表

| 用例ID | 用例名称 | 所属模块 | 前置条件 | 步骤描述 | 预期结果 | 用例等级 |
|--------|----------|----------|----------|----------|----------|----------|
| TC001 | 创建流量分析任务-全部参数正确 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入所有必填参数，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P0-冒烟测试 |
| TC002 | 创建流量分析任务-缺少必填参数Name | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】不传入必填参数Name | 【1】返回错误码<br>【2】提示缺少必填参数Name | P1-核心功能 |
| TC003 | 创建流量分析任务-缺少必填参数Frequency | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】不传入必填参数Frequency | 【1】返回错误码<br>【2】提示缺少必填参数Frequency | P1-核心功能 |
| TC004 | 创建流量分析任务-Name传入整数 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Name传入整数类型 | 【1】返回错误码<br>【2】提示参数Name类型错误 | P2-重要功能 |
| TC005 | 创建流量分析任务-Frequency传入字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Frequency传入字符串类型 | 【1】返回错误码<br>【2】提示参数Frequency类型错误 | P2-重要功能 |
| TC006 | 创建流量分析任务-传入可选参数Scenario | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入可选参数Scenario，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P3-一般功能 |
| TC007 | 创建流量分析任务-传入可选参数ResourceType | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入可选参数ResourceType，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P3-一般功能 |
| TC008 | 创建流量分析任务-传入可选参数AnalysisType | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入可选参数AnalysisType，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P3-一般功能 |
| TC009 | 创建流量分析任务-传入可选参数OneTupleRetentionDays | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入可选参数OneTupleRetentionDays，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P3-一般功能 |
| TC010 | 创建流量分析任务-传入可选参数TwoTupleRetentionDays | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入可选参数TwoTupleRetentionDays，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P3-一般功能 |
| TC011 | 创建流量分析任务-传入可选参数Remark | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】传入可选参数Remark，值合法 | 【1】返回RetCode=0<br>【2】操作成功 | P3-一般功能 |
| TC012 | 创建流量分析任务-Name为空字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Name传入空字符串 | 【1】返回错误码<br>【2】提示参数Name不能为空 | P4-边界测试 |
| TC013 | 创建流量分析任务-Name超长字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Name传入256位超长字符串 | 【1】返回错误码<br>【2】提示参数Name长度超限 | P4-边界测试 |
| TC014 | 创建流量分析任务-Frequency为0 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Frequency传入0 | 【1】返回错误码<br>【2】提示参数Frequency边界值异常 | P4-边界测试 |
| TC015 | 创建流量分析任务-Frequency为负数 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Frequency传入-1 | 【1】返回错误码<br>【2】提示参数Frequency边界值异常 | P4-边界测试 |
| TC016 | 创建流量分析任务-Scenario为空字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Scenario传入空字符串 | 【1】返回错误码<br>【2】提示参数Scenario不能为空 | P4-边界测试 |
| TC017 | 创建流量分析任务-Scenario超长字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Scenario传入256位超长字符串 | 【1】返回错误码<br>【2】提示参数Scenario长度超限 | P4-边界测试 |
| TC018 | 创建流量分析任务-ResourceType为空字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数ResourceType传入空字符串 | 【1】返回错误码<br>【2】提示参数ResourceType不能为空 | P4-边界测试 |
| TC019 | 创建流量分析任务-ResourceType超长字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数ResourceType传入256位超长字符串 | 【1】返回错误码<br>【2】提示参数ResourceType长度超限 | P4-边界测试 |
| TC020 | 创建流量分析任务-AnalysisType为空字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数AnalysisType传入空字符串 | 【1】返回错误码<br>【2】提示参数AnalysisType不能为空 | P4-边界测试 |
| TC021 | 创建流量分析任务-AnalysisType超长字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数AnalysisType传入256位超长字符串 | 【1】返回错误码<br>【2】提示参数AnalysisType长度超限 | P4-边界测试 |
| TC022 | 创建流量分析任务-OneTupleRetentionDays为0 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数OneTupleRetentionDays传入0 | 【1】返回错误码<br>【2】提示参数OneTupleRetentionDays边界值异常 | P4-边界测试 |
| TC023 | 创建流量分析任务-OneTupleRetentionDays为负数 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数OneTupleRetentionDays传入-1 | 【1】返回错误码<br>【2】提示参数OneTupleRetentionDays边界值异常 | P4-边界测试 |
| TC024 | 创建流量分析任务-TwoTupleRetentionDays为0 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数TwoTupleRetentionDays传入0 | 【1】返回错误码<br>【2】提示参数TwoTupleRetentionDays边界值异常 | P4-边界测试 |
| TC025 | 创建流量分析任务-TwoTupleRetentionDays为负数 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数TwoTupleRetentionDays传入-1 | 【1】返回错误码<br>【2】提示参数TwoTupleRetentionDays边界值异常 | P4-边界测试 |
| TC026 | 创建流量分析任务-Remark为空字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Remark传入空字符串 | 【1】返回错误码<br>【2】提示参数Remark不能为空 | P4-边界测试 |
| TC027 | 创建流量分析任务-Remark超长字符串 | /CreateNTATask | 接口服务正常可用 | 【1】调用CreateNTATask接口<br>【2】参数Remark传入256位超长字符串 | 【1】返回错误码<br>【2】提示参数Remark长度超限 | P4-边界测试 |