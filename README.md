# IP 地址查询工具

这是一个用于简单的管理和查询 IP 地址信息的命令行工具。

可以导入 IP 地址数据并提供查询功能，帮助用户快速获取指定 IP 地址的地理位置和运营商信息。

## 功能特点

- 创建和管理 SQLite 数据库
- 支持从 CSV 文件导入 IP 地址数据
- 提供 IP 地址查询功能，返回详细的地理位置信息
- 命令行界面，使用简单方便

## 数据库结构

数据库使用 SQLite，包含以下字段：

- id：主键，唯一索引
- start_ip：起始 IP 地址
- end_ip：结束 IP 地址
- country：国家
- province：省份
- city：城市
- district：区县
- isp：互联网服务提供商

## 使用方法

### 导入数据
```
python ip-tool.py import <csv文件路径>
```

### 查询 IP 信息

```
python ip-tool.py query <IP地址>
```

查询结果将显示该 IP 地址对应的：

- 国家
- 省份
- 城市
- 区县
- 运营商信息

### 帮助信息

```
python ip-tool.py --help

```

## 依赖项

- Python 3.x
- sqlite3
- ipaddress
- argparse

## 注意事项

1. 确保输入的 IP 地址格式正确（IPv4）
2. CSV 文件必须使用 UTF-8 编码
3. 导入数据时会自动创建数据库文件（ip_database.db）
4. 重复导入数据时会跳过重复的 ID

