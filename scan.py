import argparse
import os

# 当父目录包含这些子目录时，则不对父目录进行遍历
stopfile_set = {'.github', '.git', '.githooks', '.idea', 'src', 'classes', 'test', 'resources', 'logs'}
# 忽略对这些目录的遍历
ignore_set = {'zm-code', 'shareOI', 'weibo-export-test', 'weibo-export'}

def main(args):
    depth = args.d
    filepath = args.f
    if filepath == '' or depth < 0:
        print('参数错误')
        return
    # 遍历
    traverse(filepath, depth, '')

def traverse(path, depth, indentation):
    if depth == 0:
        return

    stop_flag = False
    for file in os.listdir(path):
        if file in stopfile_set:
            stop_flag = True
            break

    if stop_flag:
        return
    for file in os.listdir(path):
        if file in ignore_set:
            continue

        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            print(indentation+file_path.replace(path, ""))
            traverse(file_path, depth - 1, indentation+'|----')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=int, default='1', help='扫描深度，默认为1')
    parser.add_argument('-f', type=str, default='', help='扫描路径')
    # parser.add_argument('-f', action='store_true', help='无追加参数')
    args = parser.parse_args()

    main(args)