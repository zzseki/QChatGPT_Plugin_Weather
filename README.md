## 安装

配置完成 [QChatGPT](https://github.com/RockChinQ/QChatGPT) 主程序后使用管理员账号向机器人发送命令即可安装：

```
!plugin get <插件发布仓库地址>
```
或查看详细的[插件安装说明](https://github.com/RockChinQ/QChatGPT/wiki/5-%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8)

## 使用

可以查询国内城市未来七天的详细天气情况

前往https://www.alapi.cn/  进行注册（截至上传时是免费的）

在控制面板左侧——接口管理——更新Token密钥，点击Copy复制Token

在本插件文件夹下main.py文件中找到这行，并替换成你获取到的token（不要弄丢引号）

```
self.token = 'YOURTOKEN'  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
```

## 配置GPT

可以选择使用场景模式
提示词举例：

```
当我问你查询某个城市的天气情况，请你返回引号中的内容，不包括引号，例如查询南京今天的天气时返回“为你查询城市:南京今天的天气情况”
```



