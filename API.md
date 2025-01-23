# API Document

发送时以string格式发送，

## get_all_status

### command
```
get_all_status
```

获取所有桌所有座位的状态。\

#### response

```
1:张三;王五;?;?
```
表示座位 0 是张三，座位 1 是王五，座位 2 没有用户，座位 3 没有用户。

## get_status

### command
```
get_status
```

获取当前桌所有座位的状态。\
后接状态，以分号相隔。

#### response

```
张三;王五;?;?
```
表示座位 0 是张三，座位 1 是王五，座位 2 没有用户，座位 3 没有用户。

## add user

### Description

添加用户ID,分两个包发送。\
接ID（数字），以分号相隔。

### command
```
add_user
234
```

表示添加123用户\


### Response

`OK` 表示设置成功，`fail_out`表示添加用户后超过人数上限。

## remove user

### Description

解除用户ID，分两个包发送。 \
ID（数字），以分号相隔。

#### command

```
remove_user
234
```
表示解除123用户\

### Response

`OK` 表示设置成功，`fail_no_user`表示解除时桌上不存在该用户。
