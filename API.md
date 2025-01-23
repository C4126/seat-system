# API Document

## get_status

```
<get_status>
```

获取当前桌所有座位的状态。\
以桌号开头，后接状态，以分号相隔。

#### Example

```
<张三;王五;No;No>
```
表示座位 0 是张三，座位 1 是王五，座位 2 没有用户，座位 3 没有用户。

## add or remove user

### Description

添加或解除用户ID，第一次发送为添加，第二次发送为解除。 \
以桌号开头，后接ID（数字），以分号相隔。

#### Example

```
<234>
```
表示添加123用户\
再发送一次则解除


### Response

`OK` 表示设置成功，`fail_out`表示添加用户后超过人数上限,`fail_no_user`表示解除时桌上不存在该用户。
