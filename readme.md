# 奈咲酱-QQ聊天机器人

## 功能一览

## 快速部署 
1. 进入工作目录，clone此项目
2. 安装Python 12 以上版本
3. 在一个新的conda环境中，执行pip install -r requirements.txt
4. 在data/db中，将usr -Example.db改名为usr.db
5. 在config中填入需要使用的api密钥

## 层级结构
```
        plugins/        ✅ 插件层(顶层)
          ↓
        services/       ✅ 业务逻辑层
          ↓
        infra/          ✅ 数据访问层（数据库、API）
          ↓
        presets/        ✅ 静态预设数据
        models/         ✅ 数据结构定义
        data/           ✅ 数据存储
```
