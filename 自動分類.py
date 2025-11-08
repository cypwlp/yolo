import os
import shutil
import random
from collections import defaultdict

def split_dataset_balanced(images_path, labels_path, output_path, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1, seed=42):
    """
    均衡划分数据集，确保每个类别在训练集、验证集和测试集中分布合理
    """
    # 验证比例总和为1
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.001, "训练集、验证集、测试集比例之和必须为1"
    
    random.seed(seed)
    
    # 创建输出目录
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_path, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(output_path, 'labels', split), exist_ok=True)
    
    # 检查并复制classes.txt
    classes_file = os.path.join(labels_path, 'classes.txt')
    if os.path.exists(classes_file):
        shutil.copy2(classes_file, output_path)
        print(f"已复制classes.txt到 {output_path}")
        
        # 读取类别数量
        with open(classes_file, 'r') as f:
            classes = f.readlines()
        print(f"数据集包含 {len(classes)} 个类别: {[c.strip() for c in classes]}")
    else:
        print("警告: 未找到classes.txt文件")
    
    # 获取所有图片文件并检查对应的标签文件
    image_files = []
    valid_pairs = []
    
    for img_file in os.listdir(images_path):
        if img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
            base_name = os.path.splitext(img_file)[0]
            label_file = os.path.join(labels_path, base_name + '.txt')
            
            if os.path.exists(label_file):
                # 检查标签文件是否为空
                if os.path.getsize(label_file) > 0:
                    image_files.append(img_file)
                    valid_pairs.append((img_file, base_name))
                else:
                    print(f"警告: 标签文件 {base_name}.txt 为空，跳过")
            else:
                print(f"警告: 图片 {img_file} 没有对应的标签文件")
    
    print(f"\n有效图片-标签对: {len(valid_pairs)} 个")
    
    # 按类别分组
    class_files = defaultdict(list)
    class_counts = defaultdict(int)
    
    for img_file, base_name in valid_pairs:
        label_file = os.path.join(labels_path, base_name + '.txt')
        
        # 读取标签文件，统计类别
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        # 获取该图片中的所有类别
        classes_in_image = set()
        for line in lines:
            if line.strip():
                try:
                    class_id = int(line.strip().split()[0])
                    classes_in_image.add(class_id)
                    class_counts[class_id] += 1
                except (ValueError, IndexError):
                    print(f"警告: 标签文件 {base_name}.txt 格式错误")
        
        # 如果图片包含多个类别，我们按第一个类别分组
        if classes_in_image:
            primary_class = min(classes_in_image)  # 使用最小的类别ID作为主要类别
            class_files[primary_class].append((img_file, base_name))
        else:
            print(f"警告: 图片 {img_file} 没有有效标注")
    
    print(f"\n类别分布统计:")
    for class_id in sorted(class_counts.keys()):
        print(f"类别 {class_id}: {class_counts[class_id]} 个实例")
    
    print(f"\n按主要类别分组的图片数:")
    for class_id in sorted(class_files.keys()):
        print(f"类别 {class_id}: {len(class_files[class_id])} 张图片")
    
    # 对每个类别分别进行划分
    train_files = []
    val_files = []
    test_files = []
    
    for class_id, files in class_files.items():
        random.shuffle(files)
        
        total_class = len(files)
        train_count = int(total_class * train_ratio)
        val_count = int(total_class * val_ratio)
        
        train_files.extend(files[:train_count])
        val_files.extend(files[train_count:train_count+val_count])
        test_files.extend(files[train_count+val_count:])
    
    # 再次打乱，避免按类别顺序排列
    random.shuffle(train_files)
    random.shuffle(val_files)
    random.shuffle(test_files)
    
    print(f"\n最终划分结果:")
    print(f"训练集: {len(train_files)} 张图片")
    print(f"验证集: {len(val_files)} 张图片")
    print(f"测试集: {len(test_files)} 张图片")
    
    def copy_files(file_list, split_name):
        """复制文件到指定分割集"""
        copy_count = 0
        error_count = 0
        
        for img_file, base_name in file_list:
            # 复制图片
            img_src = os.path.join(images_path, img_file)
            img_dst = os.path.join(output_path, 'images', split_name, img_file)
            shutil.copy2(img_src, img_dst)
            
            # 复制标签
            label_file = base_name + '.txt'
            label_src = os.path.join(labels_path, label_file)
            label_dst = os.path.join(output_path, 'labels', split_name, label_file)
            
            if os.path.exists(label_src):
                shutil.copy2(label_src, label_dst)
                copy_count += 1
            else:
                print(f"错误: 未找到标签文件 {label_file}")
                error_count += 1
        
        return copy_count, error_count
    
    # 复制训练集
    print("\n正在复制训练集...")
    train_copy, train_error = copy_files(train_files, 'train')
    
    # 复制验证集
    print("正在复制验证集...")
    val_copy, val_error = copy_files(val_files, 'val')
    
    # 复制测试集
    print("正在复制测试集...")
    test_copy, test_error = copy_files(test_files, 'test')
    
    print("\n数据集划分完成！")
    print(f"输出目录: {output_path}")
    print(f"成功复制: 训练集 {train_copy}, 验证集 {val_copy}, 测试集 {test_copy}")
    
    # 验证每个集合中的文件数量
    print("\n验证文件数量:")
    for split in ['train', 'val', 'test']:
        split_images = len([f for f in os.listdir(os.path.join(output_path, 'images', split)) 
                          if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
        split_labels = len([f for f in os.listdir(os.path.join(output_path, 'labels', split)) 
                          if f.endswith('.txt')])
        
        print(f"{split}集 - 图片: {split_images}, 标签: {split_labels}, {'匹配' if split_images == split_labels else '不匹配!'}")


# 使用示例
if __name__ == "__main__":
    # 设置路径
    images_path = r'C:\Users\20250923\Desktop\YoloSource\NewFinal\images'
    labels_path = r'C:\Users\20250923\Desktop\YoloSource\NewFinal\labels'
    output_path = r'C:\Users\20250923\Desktop\YoloSource\Last'
    
    # 划分数据集（训练集70%，验证集20%，测试集10%）
    split_dataset_balanced(
        images_path=images_path,
        labels_path=labels_path,
        output_path=output_path,
        train_ratio=0.7,
        val_ratio=0.2,
        test_ratio=0.1
    )