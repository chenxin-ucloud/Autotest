### 网关接口

#### CreateIpv6Gateway - 创建IPv6网关

需要保证:

-  目标 VPC支持 IPv6
-  一个 VPC 内仅允许创建一个 IPv6 网关

##### 请求参数

| 请求参数     | 类型   | 是否必填 | 参数描述                                | 其他描述                    |
|--------------|--------|----------|-----------------------------------------|-----------------------------|
| Region       | string | 是       | 地域                                    |                             |
| ProjectId    | int    | 是       | 项目ID                                  |                             |
| request_uuid | string | 否       | 请求uuid                                |                             |
| VPCId        | string | 是       | IPv6 网关所属的VPC资源ID                |                             |
| Name         | string | 否       | IPv6 网关的名称 默认值 IPv6GateWay      |                             |
| Remark       | string | 否       | IPv6 网关的描述信息。长度为 0-256 个字符 |                             |
| Tag          | string | 否       | 业务组ID，不传将显示为Default            | 暂时只支持业务组，不接入标签 |

##### 返回参数

| 参数名称      | 类型   | 描述         |
|---------------|--------|--------------|
| Action        | string | 操作返回名称 |
| RetCode       | int    | 返回码       |
| Ipv6GatewayId | string | IPv6网关Id   |

##### 请求示例

```json
{
        "Action": "CreateIpv6Gateway",
	"Region": "cn-bj2",
        "ProjectId": "org-1xkdeb",
	"VPCId": "vnet-xxxxx", // IPv6 网关所属的VPC资源ID,
        "Name": "",
        "Tag": "",
        "Remark": ""
}
```
 
##### 返回示例

```json
{
    "Action": "CreateIpv6GatewayResponse",
    "RetCode": 0,
    "Ipv6GatewayId": "xxxxx"
}
```
 


#### DeleteIpv6Gateway - 删除IPv6网关

请求参数

```json
{
        "Action": "DeleteIpv6Gateway",
	"Region": "cn-bj2",
        "ProjectId": "org-1xkdeb",
	"Ipv6GatewayId": "ipv6gw-2ze3jv4gpdzdfkaqc31pw" // IPv6 网关资源id
}
```
 
返回参数

只返回是否删除成功

#### ModifyIpv6Gateway - 修改IPv6网关

请求参数

```json
{
        "Action": "ModifyIpv6Gateway"
	"Region": "cn-bj2",
        "ProjectId": "org-1xkdeb",
	"Ipv6GatewayId": "ipv6gw-2ze3jv4gpdzdfkaqc31pw", // IPv6 网关资源id
        "Name": "test",
        "Tag": "test",
        "Remark": "test"
}
```
 
返回参数

只返回是否修改成功

#### DescribeIpv6Gateways - 查询已创建的IPv6网关

请求参数

```json
{
        "Action": "DescribeIpv6Gateways",
	"Region": "cn-bj2",
        "ProjectId": "org-1xkdeb",
        "VPCId": "vnet-xxxxx", // IPv6 网关所属的VPC资源ID
        "Ipv6GatewayIds": "ipv6gw-2ze3jv4gpdzdfkaqc31pw" // IPv6 网关资源id
	"Limit": 20,
	"Offset": 1
}
```
 
返回参数

```json
{       
        "TotalCount": 200,
	"IPv6GateWayInfos": [
                        {
				"Name": "dddddd"
				"Description": "xxxx", // ipv6 网关的描述信息
                                "Tag": "default" // 业务组ID，不传将显示为Default
				"VPCId": "vnet-2zerqjp3g4zd4gswkqhyy",
				"CreateTime": "2025-02-12T07:05:53Z",
				"Ipv6GatewayId": "ipv6gw-2ze3jv4gpdzdfkaqc31pw"
			}
		]
	}
```
 
####  DescribeIpv6GatewayAttribute -  查询指定IPv6网关的详细信息

请求参数

```json
{
	"Region": "cn-bj2",
        "ProjectId": "org-1xkdeb",
        "VPCId": "vpc-2ze0qjoodpke45li2g1bn",
        "SubnetId": "subnet-joodpke45li2",
	"Ipv6GatewayId": "ipv6gw-2zeoc9wi666v437mdr7f6"
}
```
 
返回参数

```json
{
  "Ipv6GatewayId": "xxx",
  "Description": "",
  "Name": "MyIPv6Gateway",
  "Tag": "Production",
  "VPCId": "",
  "SubnetId": "subnet-xyz123",
  "CreateTime": 1700000000,
  "TotalCount": 2,
  "IPv6AddressInfos": [
    {
      "IPv6AddressId": "ipv6-001",
      "IPv6Address": "2001:db8::1",
      "SubnetId": "subnet-xyz123",
      "PayMode": "bandwidth",
      "Bandwidth": 100,
      "ObjectId": "instance-001",
      "OperatorName": "ChinaMobile",
      "Status": "Public",  // Public -> 出外网 Normal -> 可以出外网
      "Expire": "Expired", // 是否过期 ( Expired -> 过期 UnExpired-> 未过期 UnKnown ->未知)
      "ExpireTime": 1730000000,
      "AutoRenew": "Yes"
    }
  ]
}

```
 
### 公网带宽相关接口如下：

#### AllocateIpv6InternetBandwidth - 为IPv6地址购买公网带宽

该接口仅支持单个创建

##### 请求参数

| 请求参数      | 类型     | 是否必填 | 参数描述                                                                                                                               | 其他描述 |
|---------------|----------|----------|----------------------------------------------------------------------------------------------------------------------------------------|----------|
| Region        | string   | 是       | 地域                                                                                                                                   |          |
| ProjectId     | int      | 是       | 项目ID                                                                                                                                 |          |
| request_uuid  | string   | 否       | 请求uuid                                                                                                                               |          |
| Ipv6GatewayId | string   | 否       | ipv6网关ID（与VPCId二选一必填）                                                                                                          |          |
| VPCId         | stri  ng | 否       | vpcId（与Ipv6GatewayId二选一必填）                                                                                                       |          |
| Ipv6AddressId | string   | 是       | ipv6 id                                                                                                                                |          |
| PayMode       | string   | 否       | 付费模式；默认值 ："Bandwidth"；   枚举值：   "Bandwidth" -> 带宽计费, " Traffic" -> 流量计费                                              |          |
| ChargeType    | string   | 否       | 付费方式；默认值："Month";   枚举值：   "Dynamic" -> 按时付费，   "Month" -> 月付，   "Year" ->年付，   "Day" -> 天付，   "ThirtyDay" -> 30天 |          |
| Quantity      | int      | 否       | 购买数量                                                                                                                               |          |
| Bandwidth     | int      | 否       | 出向带宽峰值                                                                                                                           |          |
| Name          | string   | 否       | 资源名称                                                                                                                               |          |
| Remark        | string   | 否       | 备注                                                                                                                                   |          |
| Tag           | string   | 否       | 业务组；默认值为'Default'                                                                                                               |          |

##### 返回参数

| 参数名称            | 类型   | 描述                                                    |
|---------------------|--------|---------------------------------------------------------|
| Action              | string | 操作返回名称                                            |
| RetCode             | int    | 返回码                                                  |
| InternetBandwidthId | string | 开通公网带宽后，要查询的 IPv6 网关对应的公网带宽实例 ID。 |
| Ipv6Address         | string | ipv6地址                                                |
| Ipv6AddressId       | string | ipv6地址id                                              |
| RequestId           | string | 请求 ID                                                 |

#### DeleteIpv6InternetBandwidth - 删除公网带宽

该接口删除不存在资源不报错

##### 请求参数

| 请求参数            | 类型   | 是否必填 | 参数描述                                   | 其他描述 |
|---------------------|--------|----------|--------------------------------------------|----------|
| Region              | string | 是       | 地域                                       |          |
| ProjectId           | int    | 是       | 项目ID                                     |          |
| request_uuid        | string | 否       | 请求uuid                                   |          |
| InternetBandwidthId | string | 否       | ipv6公网带宽Id （与Ipv6AddressId二选一必填） |          |
| Ipv6AddressId       | string | 否       | ipv6 id（与InternetBandwidthId二选一必填）   |          |

#####  返回参数

| 参数名称 | 类型   | 描述         |
|----------|--------|--------------|
| Action   | string | 操作返回名称 |
| RetCode  | int    | 返回码       |

#### ModifyIpv6InternetBandwidth - 修改IPv6地址的公网带宽值

##### 请求参数

| 请求参数            | 类型   | 是否必填 | 参数描述                                   | 其他描述 |
|---------------------|--------|----------|--------------------------------------------|----------|
| Region              | string | 是       | 地域                                       |          |
| ProjectId           | int    | 是       | 项目ID                                     |          |
| request_uuid        | string | 否       | 请求uuid                                   |          |
| InternetBandwidthId | string | 否       | ipv6公网带宽Id （与Ipv6AddressId二选一必填） |          |
| Ipv6AddressId       | string | 否       | ipv6 id（与InternetBandwidthId二选一必填）   |          |
| Bandwidth           | int    | 否       | 要修改为的出向带宽峰值                     |          |

#####  返回参数

| 参数名称 | 类型   | 描述         |
|----------|--------|--------------|
| Action   | string | 操作返回名称 |
| RetCode  | int    | 返回码       |

#### DescribeIpv6InternetBandwidth - 查询IPv6地址的公网带宽信息

最大仅支持以vpc/ipv6网关粒度拉取所有开启外网功能的ipv6信息

最小为单IP查询

该接口是否对外暂定（以vpc侧要求为准）

##### 请求参数

| 请求参数             | 类型            | 是否必填 | 参数描述                                                                                               | 其他描述                  |
|----------------------|-----------------|----------|--------------------------------------------------------------------------------------------------------|---------------------------|
| Region               | string          | 是       | 地域                                                                                                   |                           |
| ProjectId            | int             | 是       | 项目ID                                                                                                 |                           |
| request_uuid         | string          | 否       | 请求uuid                                                                                               |                           |
| Ipv6GatewayId        | string          | 否       | ipv6网关ID（与VPCId二选一必填）                                                                          |                           |
| VPCId                | stri  ng        | 否       | vpcId（与Ipv6GatewayId二选一必填）                                                                       |                           |
| InternetBandwidthIds | array of string | 否       | 带宽Id列表；传值则按带宽Id查询信息；不传则根据vpcId/Ipv6GatewayId查询带宽信息；最大长度为100              | 是否需要根据该参数查询？？？ |
| Ipv6AddresIds        | array of string | 否       | ipv6 id列表；传值则按指定Id的ipv6Id查询带宽信息；不传则根据vpcId/Ipv6GatewayId查询带宽信息；最大长度为100 |                           |
| Limit                | int             | 否       | 数据分页值, 默认为20；指定InternetBandwidthIds / Ipv6AddresIds时不生效                                  |                           |
| Offset               | int             | 否       | 数据偏移量, 默认为0；指定InternetBandwidthIds / Ipv6AddresIds时不生效                                   |                           |

#####  返回参数

| 参数名称               | 类型                                | 描述         |  |
|------------------------|-------------------------------------|--------------|--|
| Action                 | string                              | 操作返回名称 |  |
| RetCode                | int                                 | 返回码       |  |
| InternetBandwidthInfos | array of ipv6InternetBandwidthInfos | 外网带宽信息 |  |

ipv6InternetBandwidthInfos结构体

（暂不返回绑定资源的信息）

| 参数名称            | 类型     | 描述                                                                                                                                   |
|---------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------|
| InternetBandwidthId | string   | 外网带宽id                                                                                                                             |
| Ipv6Address         | string   | ipv6 ip地址                                                                                                                            |
| Ipv6GatewayId       | string   | ipv6网关Id                                                                                                                             |
| VPCId               | stri  ng | vpcId                                                                                                                                  |
| PayMode             | string   | 付费模式；默认值 ："Bandwidth"；   枚举值：   "Bandwidth" -> 带宽计费, " Traffic" -> 流量计费                                              |
| Bandwidth           | int      | 出向带宽峰值                                                                                                                           |
| OperatorName        | string   | 线路Id                                                                                                                                 |
| Name                | string   | 资源名称                                                                                                                               |
| Remark              | string   | 备注                                                                                                                                   |
| Tag                 | string   | 业务组                                                                                                                                 |
| AutoRenew           | string   | 是否开启自动续费；  枚举值：  "Yes", "No"                                                                                                |
| ChargeType          | string   | 付费方式；默认值："Month";   枚举值：   "Dynamic" -> 按时付费，   "Month" -> 月付，   "Year" ->年付，   "Day" -> 天付，   "ThirtyDay" -> 30天 |
| ExpireTime          | int      | 过期时间（时间戳格式）                                                                                                                   |
| Expire              | string   | 是否过期 ( Expired -> 过期 UnExpired-> 未过期 UnKnown ->未知)                                                                          |
| CreateTime          | int      | 创建时间                                                                                                                               |



#### GetIPv6BandwidthRange - 查询IPv6带宽值范围

此接口主要提供给前端使用，前端和后端的各线路带宽范围应由该接口统一

（ipv6获取/校验带宽值上下限也应该直接与该接口公用一套限制）

##### 请求参数

| 请求参数       | 类型             | 是否必填 | 参数描述                                                                                  | 其他描述 |
|----------------|------------------|----------|-------------------------------------------------------------------------------------------|----------|
| Region         | string           | 是       | 地域                                                                                      |          |
| ProjectId      | int              | 是       | 项目ID                                                                                    |          |
| request_uuid   | string           | 否       | 请求uuid                                                                                  |          |
| OperatorName s | array of string  | 否       | 线路名称；不传则获取所有线路的带宽值限制；最大长度：30                                       |          |
| PayMode s      | array of  string | 否       | 计费模式；不传默认查所有计费方式；  枚举值：  "Bandwidth" -> 带宽计费, "Traffic" -> 流量计费 |          |

##### 返回参数

| 参数名称                    | 类型                                    | 描述             |  |
|-----------------------------|-----------------------------------------|------------------|--|
| Action                      | string                                  | 操作返回名称     |  |
| RetCode                     | int                                     | 返回码           |  |
| InternetBandwidthRangeInfos | array of ipv6InternetBandwidthRangeInfo | 外网带宽限制信息 |  |

ipv6InternetBandwidthRangeInfo结构体

| 参数名称     | 类型   | 描述                                                                  |
|--------------|--------|-----------------------------------------------------------------------|
| OperatorName | string | 线路名称                                                              |
| PayMode      | string | 付费模式；   枚举值：   "Bandwidth" -> 带宽计费, " Traffic" -> 流量计费 |
| BandwidthMax | int    | 购买带宽最大峰值                                                      |
| BandwidthMin | int    | 购买带宽最小峰值                                                      |

#### GetIpv6BandwidthPrice - 查询IPv6带宽价格

##### 请求参数

| 请求参数     | 类型            | 是否必填 | 参数描述                                                                                                                               | 其他描述 |
|--------------|-----------------|----------|----------------------------------------------------------------------------------------------------------------------------------------|----------|
| Region       | string          | 是       | 地域                                                                                                                                   |          |
| ProjectId    | int             | 是       | 项目ID                                                                                                                                 |          |
| request_uuid | string          | 否       | 请求uuid                                                                                                                               |          |
| OperatorName | array of string | 是       | 线路名称；不传则获取所有线路的带宽值限制；最大长度：30                                                                                    |          |
| Bandwidth    | int             | 是       | 出向带宽峰值                                                                                                                           |          |
| Quantity     | int             | 否       | 付费数量 默认 1                                                                                                                        |          |
| Count        | int             | 否       | 购买数量 默认 1                                                                                                                        |          |
| PayMode      | string          | 是       | 付费模式；默认带宽计费   枚举值：   "Bandwidth" -> 带宽计费, " Traffic" -> 流量计费                                                      |          |
| ChargeType   | string          | 是       | 付费方式；默认值："Month";   枚举值：   "Dynamic" -> 按时付费，   "Month" -> 月付，   "Year" ->年付，   "Day" -> 天付，   "ThirtyDay" -> 30天 |          |

返回参数

| 参数名称 | 类型              | 描述         |
|----------|-------------------|--------------|
| Action   | string            | 操作返回名称 |
| RetCode  | int               | 返回码       |
| PriceSet | array of PriceSet | 价格信息     |

PriceSet 结构体

| ChargeType    | string | 付费方式 |
|---------------|--------|----------|
| Price         | int    | 总价     |
| ListPrice     | int    | 原价     |
| CustomPrice   | int    | 折后价   |
| PurchaseValue | int    | 有效期   |

### GetIpv6BandwidthUpgradePrice

| 请求参数            | 类型   | 是否必填 | 参数描述     |
|---------------------|--------|----------|--------------|
| Region              | string | 是       | 地域         |
| ProjectId           | int    | 是       | 项目ID       |
| request_uuid        | string | 否       | 请求uuid     |
| InternetBandwidthId | string | 是       | 外网带宽id   |
| Bandwidth           | int    | 是       | 出向带宽峰值 |

返回参数

| 参数名称      | 类型   | 描述         |
|---------------|--------|--------------|
| Action        | string | 操作返回名称 |
| RetCode       | int    | 返回码       |
| Price         | int    | 总价         |
| CustomPrice   | int    | 折后价       |
| OriginalPrice | int    | 原价         |
| PurchaseValue | int    | 有效期       |

\======

#### CreateIpv6EgressOnlyRule - 为IPv6地址添加仅主动出规则

- 支持客户端通过 IPv6 访问外网，但是不支持外界访问 IPv6 实例

#### DeleteIpv6EgressOnlyRule - 删除仅主动出



## 三、public_ipv6_ops 接口

提供内部运维能力的服务

#### AddPublicIPv6BWNonStandard - 添加公网ipv6的带宽非标限速

此接口主要提供给sre同学使用，以下为内部网关调用请求

##### 请求参数

| 请求参数       | 类型                     | 是否必填 | 参数描述                     | 其他描述 |
|----------------|--------------------------|----------|------------------------------|----------|
| RegionId       | int                      | 是       | 地域Id                       |          |
| request_uuid   | string                   | 否       | 请求uuid                     |          |
| NonStandardCfg | array of  NonStandardCfg | 否       | 非标限速配置信息；最大长度100 |          |

##### NonStandardCfg

| 请求参数       | 类型   | 是否必填 | 参数描述                                                              | 其他描述 |
|----------------|--------|----------|-----------------------------------------------------------------------|----------|
| CompanyId      | int    | 是       | 资源所属的公司Id                                                      |          |
| AccountId      | int    | 否       | 资源所属的项目Id；除LimitingObject为3表示公司Id时可不传，其余场景为必填 |          |
| Source         | int    | 是       | 限速规则来源；1:欠费、2:用户操作、3:运维操作、4:产品操作                  |          |
| LimitingObject | int    | 是       | 限速对象；1:ipv6bwId，2:项目Id，3:公司Id                                 |          |
| Resource       | string | 是       | 被限速的对象Id                                                        |          |
| Ingress        | int    | 是       | 入向限速; 单位kbps                                                    |          |
| Egress         | int    | 是       | 出向限速; 单位kbps                                                    |          |
| ExpirationTime | int    | 否       | 限速规则过期时间; 不传默认封禁 10 年；时间戳格式                       |          |
| OperatorRemark | string | 否       | 操作备注；                                                             |          |

##### 返回参数

| 参数名称 | 类型   | 描述         |  |
|----------|--------|--------------|--|
| Action   | string | 操作返回名称 |  |
| RetCode  | int    | 返回码       |  |



#### DelPublicIPv6BWNonStandard - 删除公网ipv6的带宽非标限速

此接口主要提供给sre同学使用，以下为内部网关调用请求

##### 请求参数

| 请求参数       | 类型                    | 是否必填 | 参数描述         | 其他描述 |
|----------------|-------------------------|----------|------------------|----------|
| RegionId       | int                     | 是       | 地域Id           |          |
| request_uuid   | string                  | 否       | 请求uuid         |          |
| NonStandardCfg | array of NonStandardCfg | 否       | 非标限速配置信息 |          |

##### NonStandardCfg

| 请求参数       | 类型   | 是否必填 | 参数描述                                                               | 其他描述 |
|----------------|--------|----------|------------------------------------------------------------------------|----------|
| CompanyId      | int    | 是       | 资源所属的公司Id                                                       |          |
| AccountId      | int    | 否       | 资源所属的项目Id；除LimitingObject为3表示公司Id时可不传，其余场景为必填  |          |
| Source         | int    | 否       | 限速规则来源；1:欠费、2:用户操作、3:运维操作；不传则删除所有来源的非标限速 |          |
| LimitingObject | int    | 是       | 限速对象；1:ipv6bwId，2:项目Id，3:公司Id                                  |          |
| Resource       | string | 是       | 被限速的对象Id                                                         |          |

##### 返回参数

| 参数名称 | 类型   | 描述         |  |
|----------|--------|--------------|--|
| Action   | string | 操作返回名称 |  |
| RetCode  | int    | 返回码       |  |



#### UpdatePublicIPv6BWNonStandard - 修改公网ipv6的带宽非标限速

此接口主要提供给sre同学使用，以下为内部网关调用请求

##### 请求参数

| 请求参数       | 类型           | 是否必填 | 参数描述                     | 其他描述 |
|----------------|----------------|----------|------------------------------|----------|
| RegionId       | int            | 是       | 地域Id                       |          |
| request_uuid   | string         | 否       | 请求uuid                     |          |
| NonStandardCfg | NonStandardCfg | 否       | 非标限速配置信息；最大长度100 |          |

##### NonStandardCfg

| 请求参数       | 类型   | 是否必填 | 参数描述                                                                         | 其他描述 |
|----------------|--------|----------|----------------------------------------------------------------------------------|----------|
| CompanyId      | int    | 是       | 资源所属的公司Id；不允许修改                                                      |          |
| AccountId      | int    | 否       | 资源所属的项目Id；除LimitingObject为3表示公司Id时可不传，其余场景为必填；不允许修改 |          |
| Source         | int    | 是       | 限速规则来源；1:欠费、2:用户操作、3:运维操作；不允许修改                             |          |
| LimitingObject | int    | 是       | 限速对象；1:ipv6bwId，2:项目Id，3:公司Id；不允许修改                                 |          |
| Resource       | string | 是       | 被限速的对象Id；不允许修改                                                        |          |
| Ingress        | int    | 否       | 入向限速; 单位kbps；传值非0会覆盖之前的数据                                       |          |
| Egress         | int    | 否       | 出向限速; 单位kbps；传值非0会覆盖之前的数据                                       |          |
| ExpirationTime | int    | 否       | 限速规则过期时间; 不传默认封禁 10 年；时间戳格式；传值非0会覆盖之前的数据          |          |
| OperatorRemark | string | 否       | 操作备注；传值非空会覆盖之前的记录                                                |          |

##### 返回参数

| 参数名称 | 类型   | 描述         |  |
|----------|--------|--------------|--|
| Action   | string | 操作返回名称 |  |
| RetCode  | int    | 返回码       |  |



#### GetPublicIPv6BWNonStandard - 获取公网ipv6的带宽非标限速

此接口主要提供给sre同学使用，以下为内部网关调用请求

##### 请求参数

Source、LimitingObject、Resource都不传则查全量数据

| 请求参数       | 类型   | 是否必填 | 参数描述                                                           | 其他描述 |
|----------------|--------|----------|--------------------------------------------------------------------|----------|
| RegionId       | int    | 是       | 地域Id                                                             |          |
| request_uuid   | string | 否       | 请求uuid                                                           |          |
| CompanyId      | int    | 否       | 资源所属的公司Id ；不传则根据其他参数值查询                         |          |
| AccountId      | int    | 否       | 资源所属的项目Id ；不传则根据其他参数值查询                         |          |
| Source         | int    | 否       | 限速规则来源；1:欠费、2:用户操作、3:运维操作；不传则根据其他参数值查询 |          |
| LimitingObject | int    | 否       | 限速对象；1:ipv6bwId，2:项目Id，3:公司Id；不传则根据其他参数值查询     |          |
| Resource       | string | 否       | 被限速的对象Id；不传则根据其他参数值查询                            |          |

##### 

##### 返回参数

| 参数名称            | 类型                    | 描述         |  |
|---------------------|-------------------------|--------------|--|
| Action              | string                  | 操作返回名称 |  |
| RetCode             | int                     | 返回码       |  |
| NonStandardCfgInfos | array of NonStandardCfg | 非标限速信息 |  |

##### NonStandardCfg

| 请求参数       | 类型   | 参数描述                                  | 其他描述 |
|----------------|--------|-------------------------------------------|----------|
| CompanyId      | int    | 资源所属的公司Id                          |          |
| AccountId      | int    | 资源所属的项目Id                          |          |
| Source         | int    | 限速规则来源；1:欠费、2:用户操作、3:运维操作 |          |
| LimitingObject | int    | 限速对象；1:ipv6bwId，2:项目Id，3:公司Id     |          |
| Resource       | string | 被限速的对象Id                            |          |
| Ingress        | int    | 入向限速; 单位kbps                        |          |
| Egress         | int    | 出向限速; 单位kbps                        |          |
| ExpirationTime | int    | 限速规则过期时间；时间戳格式               |          |
| InsertTime     | int    | 添加时间                                  |          |
| UpdateTime     | int    | 修改时间                                  |          |
| OperatorRemark | string | 操作备注；                                 |          |
