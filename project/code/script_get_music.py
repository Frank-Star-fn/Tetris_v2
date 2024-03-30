import os

def list_files_in_directory(directory):
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print("Error: '{}' 不是一个有效的目录.".format(directory))
        return
    
    # 获取目录中的所有文件名
    files = os.listdir(directory)
    
    # 输出文件名
    for file in files:
        print('r"music\\'+file+'",')

# 指定目标文件夹路径
directory_path = r"C:\myfile\program\py\game\Tetris_v2\music"

# 调用函数来列出目录中的所有文件名
list_files_in_directory(directory_path)
