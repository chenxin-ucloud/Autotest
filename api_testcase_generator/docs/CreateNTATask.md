# 创建流量分析任务-CreateNTATask

创建流量分析任务

# Request Parameters
|Parameter name|Type|Description|Required|
|---|---|---|---|
|Name|string|任务名称|**Yes**|
|Frequency|int|采样频率，单位秒|**Yes**|
|ResourceLabel.n.Key|string|绑定的资源标签key|No|
|ResourceLabel.n.Value|string|绑定的资源标签Value|No|
|Scenario|string|分析场景 仅用于展示|No|
|ResourceType|string|资源类型 仅用于展示|No|
|AnalysisType|string|流量分析类型 高精度流量统计 长周期流量统计 用于页面展示|No|
|OneTupleRetentionDays|int|一元组保存天数，单位天|No|
|TwoTupleRetentionDays|int|二元组保存天数，单位天|No|
|Remark|string|备注|No|

# Response Elements
|Parameter name|Type|Description|Required|
|---|---|---|---|
|RetCode|int|返回码|**Yes**|
|Action|string|操作名称|**Yes**|
|ResourceID|string|资源ID（from资源系统）|No|

# Request Example
```
https://api.ucloud.cn/?Action=CreateNTATask
&Name=HjLnbVhU
&ResourceLabel.N=ntkoMbdK
&Frequency=1
&Scenario=RCVnjpef
&ResourceType=IKCjyqII
&AnalysisType=uepnFTnt
&OneTupleRetentionDays=4
&TwoTupleRetentionDays=7
&Remark=yiAmLyEB
&ResourceLabel.n.Value=lAzWKIDT
```

# Response Example
```
{
    "Action": "CreateNTATaskResponse", 
    "ResourceID": "VXJCtajV", 
    "RetCode": 0
}
```

