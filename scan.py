import argparse
import os

# 当父目录包含这些子目录时，则不对父目录进行遍历
stopfile_set = {'.github', '.git', '.githooks', '.idea', 'src', 'classes', 'test', 'resources', 'logs', 'css', 'LICENSE', 'pom.xml'}
# 忽略对这些目录的遍历
ignore_set = {'zm-code', 'shareOI', 'weibo-export-test', 'weibo-export'}
# 忽略的文件
ignore_files = {'.DS_Store'}


def main(args):
    depth = args.d
    filepath = args.f
    if filepath == '' or depth < 0:
        print('参数错误')
        return
    exclude = args.exclude_format
    exclude_format_set = set()
    if exclude != '':
        arr = exclude.split(',')
        exclude_format_set = set(arr)
    # 遍历
    traverse(filepath, depth, '', filepath, args.include_files, exclude_format_set)

def traverse(path, depth, indentation, base_path, include_files, exclude_format):
    if depth == 0:
        return ''

    # print(path)
    readme_name = ''
    stop_flag = False
    # 如果当前目录文件中有 readme.md，则读取相关内容
    for file in os.listdir(path):
        if file.lower() == 'readme.md':
            readme_name = getname_by_readme(os.path.join(path, file))
            break

    if readme_name == '':
        for file in os.listdir(path):
            if file in stopfile_set:
                stop_flag = True
                break

    if stop_flag or readme_name != '':
        print(indentation + path.replace(base_path, '') + readme_name)
        return readme_name

    for file in os.listdir(path):
        if file in ignore_set:
            continue

        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            name = traverse(file_path, depth - 1, indentation + '|----', base_path, include_files, exclude_format)
            if name == '':
                print(indentation+file_path.replace(base_path, ''))
        if include_files and os.path.isfile(file_path):
            if file in ignore_files:
                continue
            if file.split('.')[-1] in exclude_format:
                continue
            print(indentation + file_path.replace(base_path, ''))
    return ''

def getname_by_readme(readme_file):
    lines = []
    with open(readme_file, 'r') as file:
        for line in file:
            lines.append(line.replace("\n", ""))
    # 返回可能的文件名
    first_ctnt = ''
    for i in range(len(lines)):
        line = lines[i]
        if (line.strip() == ''
            or line.strip().startswith('===')
            or line.strip().startswith('[!')
            or line.strip().startswith('![')
            or line.strip().startswith('<html>')
            or line.strip().startswith('<') and line.find('<h1') == -1
            or line.find('](') != -1
            or line.find('简介') != -1
            or line.find('前言') != -1
            or line.find('目录') != -1
            or line.find('介绍') != -1
            or line.find('技术') != -1
            or line.find('版本') != -1
            or line.find('项目地址') != -1
            or line.find('项目结构') != -1):
            lines[i] = ''
            continue

        if (first_ctnt == '' and (
                line.strip().startswith('# ')
                or line.find('<h1') != -1 or line.find('<h2') != -1 or line.find('<h3') != -1
        )):
            first_ctnt = line
            break
    # 如果第一遍扫描之后未找到合适的行作为title，则再遍历一遍
    if first_ctnt == '':
        for i in range(len(lines)):
            if lines[i] != '':
                first_ctnt = lines[i]
                break
    return first_ctnt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=int, default='3', help='扫描深度，默认为3')
    parser.add_argument('-f', type=str, default='', help='扫描路径')
    parser.add_argument('--include_files', action='store_true', default=False, help='包括一般文件')
    parser.add_argument('--exclude_format', type=str, default='', help='不扫描的文件类型，以,隔开')
    args = parser.parse_args()

    main(args)