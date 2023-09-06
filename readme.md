## 一、工具功能说明

- 仅对源仓库只做读取、拉取操作。
- 支持目标仓库项目自动创建。
- 支持目标仓库群组自动创建。
- 支持分支创建、修改同步，不支持删除。
- 支持标签创建、修改同步，不支持删除。
- 支持目标仓库与源仓库文件同步变动。
- 支持本地缓存，避免每次重启后全量从头拉取。
- 支持配置文件动态修改，无需重启服务。
- 支持且只支持白名单过滤项目。 
- 支持

## 二、基本环境安装

#### 1、基础环境

- centos7.6及以上、2核8G，存储不小于源库代码存储容量。
- 建议 git 1.8.3
- 开发者使用python3.7其他版本未做兼容性测试

#### 2、依赖安装
 python安装自行搜索解决


#### 3、依赖库安装

pip3 install -r requirements.txt 

## 三、配置文件说明

配置文件为yml格式

```yaml
source_domain: source.example.gitlab.com #源地址
source_token: xxxxxx   
source_protocol: http/https    # 暂时只支持http和https方式
target_domain: target.example.gitlab.com   #目标地址
target_protocol: http/https # 暂时只支持http和https方式
target_token: *****
target_api_token: *****
project_list:    #项目白名单
  - root/test
  - demo
webhook_token: *****   #源gitlab的webhook token
webhook_port: 6000
repo_base_path: ./repo/   # 本地缓存代码库地址
log_path: ./logs   #日志文件地址
lock_path: /lock   # 防止重复执行的锁定文件地址
```



## 四、启动

#### **1、启动文件**

```ini
[Unit]
Description=gitsync deamon
After=rc-local.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/data/gitrsync/app
ExecStart=/usr/bin/python3 gitsync.py -c ./config.yml
Restart=always

[Install]
WantedBy=multi-user.target
```

完成编辑后

```shell
systemctl daemon-reload
```



#### 2、启动

systemctl start gitsync



## 五、后续优化
