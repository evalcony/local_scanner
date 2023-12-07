# local_scanner
- 对本地目录进行扫描（限定深度）。
- 对于目录下包含 readme.md 的，视为代码项目，会自动提取 readme.md 中内容，进行标注。
- 包含若干截止扫描条件，视为扫描终点，防止扫描非重要目录。

使用方法
```commandline
python3 scan.py -f '/Users/evalcony/coding' -d 4 > result.txt
```

参数介绍

- `-d` 表示扫描深度，默认为3。
- `-f` 表示扫描路径。
- `--include_files` 也对文件进行扫描。
- `--exclude_format` 排除扫描某些类型的文件，以`,`隔开，无空格。