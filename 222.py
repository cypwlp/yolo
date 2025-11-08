import os

def check_and_create_missing_files():
    # 设置文件夹路径
    folder_path = r"C:\Users\20250923\Desktop\YoloSource\Initial\labels"
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在！")
        return
    
    # 获取当前文件夹中所有的txt文件
    existing_files = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            # 提取数字部分（去掉.txt扩展名）
            try:
                number = int(filename[:-4])  # 去掉.txt，转换为整数
                existing_files.add(number)
            except ValueError:
                continue  # 如果文件名不是纯数字，跳过
    
    # 找出缺失的文件
    missing_files = []
    for i in range(1, 1202):  # 001到1201
        if i not in existing_files:
            missing_files.append(i)
    
    # 创建缺失的文件
    created_count = 0
    for number in missing_files:
        # 格式化为三位数，不足前面补零
        filename = f"{number:03d}.txt"
        file_path = os.path.join(folder_path, filename)
        
        # 创建空的txt文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                pass  # 创建空文件
            print(f"已创建缺失文件: {filename}")
            created_count += 1
        except Exception as e:
            print(f"创建文件 {filename} 时出错: {e}")
    
    # 输出结果摘要
    print(f"\n=== 操作完成 ===")
    print(f"检查范围: 001.txt 到 1201.txt")
    print(f"现有文件数量: {len(existing_files)}")
    print(f"缺失文件数量: {len(missing_files)}")
    print(f"成功创建文件数量: {created_count}")
    
    if missing_files:
        print(f"\n缺失的文件有: {len(missing_files)} 个")
        # 如果缺失文件太多，只显示前20个
        if len(missing_files) > 20:
            print("前20个缺失文件:", [f"{n:03d}.txt" for n in missing_files[:20]])
            print("... (还有更多)")
        else:
            print("缺失文件:", [f"{n:03d}.txt" for n in missing_files])

if __name__ == "__main__":
    check_and_create_missing_files()