# API Document

## GET `/api/get_status`

GET Parameters:

| Parameter Name | Value                          |
| -------------- | ------------------------------ |
| `tableid`      | Int. The ID of requested table |

GET Response:

四个人名，用分号连接。本接口每个终端会每秒请求一次，按座位号排序，如果没有用户，使用空表示。

Example:

```
张三;李四;;王五
```

## POST `api/add_user`

POST Parameters:

| Parameter Name | Value                          |
| -------------- | ------------------------------ |
| `tableid`      | Int. The ID of requested table |

POST Body:

一个数字和一个编号，用分号连接。

Example:

```
3;123456789
```

该请求表示座位 3（座位号从 0 开始）被卡号为 123456789 的用户占领了
