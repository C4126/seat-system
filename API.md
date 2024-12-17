# API Document

## GET `/api/get_status`

### Description

获取当前桌所有座位的状态。

### Parameters

| Name      | Value            |
| --------- | ---------------- |
| `tableid` | Int. 当前桌的 ID |

### Response

四个人名，用分号连接。本接口每个终端会每秒请求一次，按座位号排序；如果没有用户，使用空表示；如果被 `api/add_user` 占座，则使用 `*` 表示。

#### Example

```
张三;王五;*;;
```

该响应表示座位 0 是张三，座位 1 是王五，座位 2 被占了（），座位 3 没有用户。

## POST `api/add_user`

### Description

为给定的人数占座，在一定时间内如果没有调用 `api/set_user`，则应该自动解除占用。

### Parameters

| Name      | Value            |
| --------- | ---------------- |
| `tableid` | Int. 当前桌的 ID |

### Body:

一个数字，表示占座的人数。

#### 例子

```
3
```

该请求表示占座 3 个人。

### 响应

`OK` 表示添加成功，`FAIL` 表示添加失败。

## POST `api/cancel_add_user`

### Description

取消用户占用。

### Parameters

| Name      | Value            |
| --------- | ---------------- |
| `tableid` | Int. 当前桌的 ID |

### Body:

空。

### 响应

`OK` 表示取消成功，`FAIL` 表示取消失败。

## POST `api/set_user`

### Description

设定用户的 ID。本请求保证在 `api/add_user` 之后调用该请求指定的次数，如果没有，则应该失败。

### Parameters

| Name      | Value            |
| --------- | ---------------- |
| `tableid` | Int. 当前桌的 ID |

### Body

一个编号，表示用户的 ID。

#### Example

```
123456789
```

该请求表示本桌被 ID 为 123456789 的用户占用了。

### Response

`OK` 表示设置成功，`FAIL` 表示设置失败。

## POST `api/delete_user`

### Description

删除给定 ID 的用户。

### Parameters

| Name      | Value            |
| --------- | ---------------- |
| `tableid` | Int. 当前桌的 ID |

### Body

一个编号，表示用户的 ID。

#### Example

```
123456789
```

该请求删除了 ID 为 123456789 的用户。

### Response

`OK` 表示删除成功，`FAIL` 表示删除失败。
