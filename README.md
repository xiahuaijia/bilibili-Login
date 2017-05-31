哔哩哔哩 登录API参数
==
使用B站Api js 提取出来的核心
--
BY AceSheep 2017年3月17日  from minilogin

ajax.php 接口参数  全部都是Get请求  编码UTF-8

##### 简单的说几句

## B站POST 参数有变化,注意模拟准确 2017-05-31


这个API把计算交给了服务器,会返回一个计算结果给软件.
好处是 个个语言都不需要写 RSA 算法啦.例如:shell脚本,C# (C#的公钥是XML格式)

当然在把视频的算法逆向出来前,ajax.php 暂时不放出来.如果你担心安全问题,你可以自己写一个.

#### 现已提供
选择分支进行查看

|语言|状态|时间(UTC+8)|备注|
|---|---|----|----|
|PHP|![](http://www.acesheep.com/bilibili_Login/status/failing.svg?1492106887)|2017-03-21 17:30:00|暂时未公布
|JavaScript|![](http://www.acesheep.com/bilibili_Login/status/passing.svg?1492106887)|2017-03-16 20:28:54|AceSheep
|C#|![](http://www.acesheep.com/bilibili_Login/status/passing.svg?1492106887)|2017-04-20 15:54:28|丶小C 提供
|Python|![](http://www.acesheep.com/bilibili_Login/status/passing.svg?1492106887)|2017-02-06 12:34:55|[ztcaoll222 提供](https://github.com/ztcaoll222/bilibili_login)

# 获取验证码captcha:

##### 需要的参数:

|参数|语法|备注|
|---|---|----|
|act|captcha|固定为captcha|
|ts|1 或者 !=0 |1时返回 Base64 后的图片数据  不等于0时 网页输出图片|

返回验证码~

例子 http://www.acesheep.com/bilibili_Login/ajax.php?act=captcha&ts=1   Base64 后的图片数据
     http://www.acesheep.com/bilibili_Login/ajax.php?act=captcha&ts=3   网页输出Base64编码图片data:image/jpeg;base64,


# 获取密钥:getkey
##### 需要的参数:

|参数|语法|备注|
|---|---|----|
|act|getkey|固定为getkey
|ts|13位Unix时间戳|1489555973312

返回 json 文本

例子 http://www.acesheep.com/bilibili_Login/ajax.php?act=getkey&ts=1489555973312<br>
例子返回 
```
{"hash":"49d28ca8f5c10f6b","key":"-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdScM09sZJqFPX7bvmB2y6i08J\nbHsa0v4THafPbJN9NoaZ9Djz1LmeLkVlmWx1DwgHVW+K7LVWT5FV3johacVRuV98\n37+RNntEK6SE82MPcl7fA++dmW2cLlAjsIIkrX+aIvvSGCuUfcWpWFy3YVDqhuHr\nNDjdNcaefJIQHMW+sQIDAQAB\n-----END PUBLIC KEY-----\n"}
```

# 获取密钥:getpasswd
##### 需要的参数:

|参数|语法|备注|
|---|---|----|
|act|getpasswd|固定为getpasswd
|ts|Base64编码的密码|MTIzYWJj
|hash|本地请求获得的hash|49d28ca8f5c10f6b
|sign|校验和|后附算法

返回 文本  每次返回值不一样

例子  http://www.acesheep.com/bilibili_Login/ajax.php?act=getpasswd&ts=dGVzdA==&hash=1dc79af795a0d88b&sign=7bc42fbc33446bd7ca6f03b574bbb4eb

例子返回

```
cXb+O1QW5IhqMLYAee1tzLQ6TGq8OabCIFJUeQZKqoN1WoTIPZ+TBQm/zy8/EczroqcS/dlI/s/hX+aTRPmlsUkZGNqxjL8n9Sk9QO6zVEnCwGNZWBGyZaJSkKho0PdHBHpQmuZRIwt1YJ7dVSLAxYpmiIA61Lam6O5SwuLpaBU=
```
提示!!!!!!!!!!!!!
加密后的密码有效期为20秒  hash有效期为20秒!!!!!

`sign 算法(服务器)`
```php
          $appkey = "MjNnRTBSZWI4blkzbDNSZ251Zm8="; // AppKey 用了Base64 加密<br>
          $str ='passwd='.base64_decode($passwd).'&hash='.$hash.'&appkey='.base64_decode($appkey);
```
`说明(客户端)~    MD5一下("passwd=" + 密码 + "&hash=" + hash值 + "&appkey=" + base64_decode解码的appkey)`


# 错误代码说明:

|错误代码|位置|原因|
|---|---|----|
|参数错误|全局|act  或 ts 值为空
|参数错误100|全局|act  没有匹配的参数
|参数错误102|captcha|ts值为空
|参数错误103 or 104|getpasswd|hash 或 sign 值为空
|参数错误105|getpasswd|sign 错误

