import os
import random
import shutil
import uuid


def shuffle_images_and_labels(images_dir, labels_dir, output_images_dir, output_labels_dir):
    """随机打乱图片和标签文件，使用UUID重命名，彻底改变命名方式.

    Args:
        images_dir: 原始图片目录
        labels_dir: 原始标签目录
        output_images_dir: 输出图片目录
        output_labels_dir: 输出标签目录
    """
    # 确保输出目录存在
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)

    # 获取所有图片文件（只处理PNG文件）
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(".png")]

    # 创建图片和标签的对应列表
    pairs = []
    for img_file in image_files:
        # 获取不带扩展名的文件名
        base_name = os.path.splitext(img_file)[0]
        label_file = base_name + ".txt"
        label_path = os.path.join(labels_dir, label_file)

        # 检查对应的标签文件是否存在
        if os.path.exists(label_path):
            pairs.append((img_file, label_file))
        else:
            print(f"警告: 找不到标签文件 {label_file} 对应的图片 {img_file}")

    print(f"找到 {len(pairs)} 对有效的图片-标签文件")

    # 随机打乱
    random.shuffle(pairs)
    print("文件顺序已随机打乱")

    # 使用UUID重新命名并复制文件
    uuid_mapping = {}  # 用于记录原始文件名和UUID的对应关系

    for i, (img_file, label_file) in enumerate(pairs, 1):
        # 为每对文件生成唯一的UUID
        file_uuid = str(uuid.uuid4())

        # 记录映射关系
        base_name = os.path.splitext(img_file)[0]
        uuid_mapping[base_name] = file_uuid

        # 原始文件路径
        old_img_path = os.path.join(images_dir, img_file)
        old_label_path = os.path.join(labels_dir, label_file)

        # 新文件路径（使用UUID命名）
        new_img_path = os.path.join(output_images_dir, f"{file_uuid}.png")
        new_label_path = os.path.join(output_labels_dir, f"{file_uuid}.txt")

        # 复制文件
        shutil.copy2(old_img_path, new_img_path)
        shutil.copy2(old_label_path, new_label_path)

        if i % 100 == 0:
            print(f"已处理 {i}/{len(pairs)} 个文件")

    # 保存文件名映射关系，以便后续需要时参考
    mapping_file = os.path.join(os.path.dirname(output_images_dir), "filename_mapping.txt")
    with open(mapping_file, "w", encoding="utf-8") as f:
        f.write("原始文件名 -> UUID文件名\n")
        for original, new_uuid in uuid_mapping.items():
            f.write(f"{original} -> {new_uuid}\n")

    print("完成！文件已随机打乱并使用UUID重新命名")
    print(f"输出目录: {output_images_dir}, {output_labels_dir}")
    print(f"文件名映射已保存到: {mapping_file}")

    # 显示一些示例
    output_images = [f for f in os.listdir(output_images_dir) if f.lower().endswith(".png")]
    print("\n输出目录中的前5个文件示例:")
    for i, filename in enumerate(output_images[:5]):
        print(f"  {i + 1}. {filename}")


def main():
    # 设置路径
    images_dir = r"C:\Users\20250923\Desktop\YoloSource\Initial\images"
    labels_dir = r"C:\Users\20250923\Desktop\YoloSource\Initial\labels"

    # 输出目录（可以根据需要修改）
    output_images_dir = r"C:\Users\20250923\Desktop\YoloSource\NewFinal\images"
    output_labels_dir = r"C:\Users\20250923\Desktop\YoloSource\NewFinal\labels"

    # 执行打乱操作
    shuffle_images_and_labels(images_dir, labels_dir, output_images_dir, output_labels_dir)


if __name__ == "__main__":
    main()
