重复文件检查工具
===
# 功能
通过检查指定路径下所有文件的散列值判断重复文件

# 使用
## 源代码
### 环境要求
- python3.11+
### 使用方法
1. 拉取代码\
`git clone https://github.com/xzb23/check_duplicate_files.git`
2. `python app.py [-P] [--fsize]`
## 可执行文件（仅Windows提供）
1. 下载程序
2. 添加环境变量（可选）
3. 在终端中执行\
`python app.py [-P] [--fsize]`

# 参数选项
```
-h, --help  查看帮助
-P, --path  指定检查的目录, 默认当前工作目录
--fsize     只打印文件大小大于fsize Byte的重复文件, 默认10240Byte
```

# 更新计划
- [ ] GUI界面（Windows）
- [ ] 支持一键清理/整理重复文件
- [ ] 支持对结果列表重排序