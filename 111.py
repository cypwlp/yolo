import os
import re
import shutil


def group_files_by_range(base_path, group_size=50):
    """将数字名称的文件按照指定范围分组.

    Args:
        base_path: 包含数字文件的根目录路径
        group_size: 每组包含的文件数量，默认为50
    """
    # 获取所有项目
    all_items = os.listdir(base_path)

    # 筛选出数字名称的文件
    number_files = []
    for item in all_items:
        item_path = os.path.join(base_path, item)
        if os.path.isfile(item_path):  # 检查是否是文件
            # 使用正则表达式匹配纯数字文件名（不包括扩展名）
            file_name_without_ext = os.path.splitext(item)[0]
            if re.match(r"^\d+$", file_name_without_ext):
                number_files.append(item)

    if not number_files:
        print("未找到数字名称的文件")
        return

    # 将文件名转换为整数并排序（只取数字部分）
    number_files = sorted(number_files, key=lambda x: int(os.path.splitext(x)[0]))

    print(f"找到 {len(number_files)} 个数字文件")
    print(f"文件列表: {number_files[:10]}...")  # 只显示前10个

    # 按范围分组
    for i in range(0, len(number_files), group_size):
        start_num = int(os.path.splitext(number_files[i])[0])
        end_num = int(os.path.splitext(number_files[min(i + group_size - 1, len(number_files) - 1)])[0])

        # 创建分组文件夹名称
        group_folder_name = f"{start_num:03d}-{end_num:03d}"
        group_folder_path = os.path.join(base_path, group_folder_name)

        # 创建分组文件夹
        if not os.path.exists(group_folder_path):
            os.makedirs(group_folder_path)
            print(f"创建分组文件夹: {group_folder_name}")

        # 移动该范围内的文件到分组文件夹中
        moved_count = 0
        for j in range(i, min(i + group_size, len(number_files))):
            file_name = number_files[j]
            old_path = os.path.join(base_path, file_name)
            new_path = os.path.join(group_folder_path, file_name)

            try:
                shutil.move(old_path, new_path)
                moved_count += 1
                print(f"移动文件: {file_name} -> {group_folder_name}/")
            except Exception as e:
                print(f"移动文件 {file_name} 时出错: {e}")

        print(f"分组 {group_folder_name} 完成，移动了 {moved_count} 个文件\n")


def main():
    # 使用原始字符串（在字符串前加r）
    base_directory = r"C:\Users\20250923\Desktop\YoloSource\Initial\img"

    # 检查路径是否存在
    if not os.path.exists(base_directory):
        print("指定的路径不存在！")
        return

    # 设置每组大小
    try:
        group_size = int(input("请输入每组包含的文件数量 (默认50): ") or "50")
    except ValueError:
        group_size = 50
        print("使用默认分组大小: 50")

    print(f"\n开始处理目录: {base_directory}")
    print(f"分组大小: {group_size}\n")

    # 执行分组操作
    group_files_by_range(base_directory, group_size)

    print("文件分组完成！")


if __name__ == "__main__":
    main()
