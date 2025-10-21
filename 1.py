import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import albumentations as A

class CEDefectGenerator:
    def __init__(self, output_path, base_size=200):
        self.output_path = output_path
        self.base_size = base_size
        os.makedirs(output_path, exist_ok=True)
        
        # 创建子目录用于不同缺陷类型
        self.defect_types = [
            "partial_c", "partial_e", "size_error_small", "size_error_large",
            "ratio_error", "perspective_error", "distortion_error", 
            "rotation_error", "blur_error", "noise_error", "stretch_error"
        ]
        for defect_type in self.defect_types:
            os.makedirs(os.path.join(output_path, defect_type), exist_ok=True)
    
    def create_standard_ce(self):
        """创建标准的CE标志"""
        size = self.base_size
        img = Image.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        # 绘制C和E的基本形状
        # C字母
        margin = size // 10
        c_radius = size // 3
        c_center = (size // 2 - c_radius // 2, size // 2)
        draw.arc([c_center[0] - c_radius, c_center[1] - c_radius,
                 c_center[0] + c_radius, c_center[1] + c_radius],
                 start=30, end=330, fill='black', width=size//20)
        
        # E字母
        e_width = size // 20
        e_height = c_radius * 2
        e_x = size // 2 + c_radius // 2
        e_y = size // 2 - c_radius
        
        # E的竖线
        draw.rectangle([e_x, e_y, e_x + e_width, e_y + e_height], fill='black')
        # E的横线
        draw.rectangle([e_x, e_y, e_x + e_width * 3, e_y + e_width], fill='black')
        draw.rectangle([e_x, size//2 - e_width//2, e_x + e_width * 3, size//2 + e_width//2], fill='black')
        draw.rectangle([e_x, e_y + e_height - e_width, e_x + e_width * 3, e_y + e_height], fill='black')
        
        return np.array(img)
    
    def generate_partial_c(self, base_image):
        """生成只有C的不完整样本"""
        h, w = base_image.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # 创建一个掩码来保留C部分，移除E部分
        c_radius = w // 3
        c_center = (w // 2 - c_radius // 2, h // 2)
        cv2.circle(mask, c_center, c_radius, 255, -1)
        
        # 应用掩码
        result = base_image.copy()
        result[mask == 0] = 255  # 将非C区域设为白色
        
        return result
    
    def generate_partial_e(self, base_image):
        """生成只有E的不完整样本"""
        h, w = base_image.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # 创建一个掩码来保留E部分
        e_width = w // 20
        e_height = w // 3 * 2
        e_x = w // 2 + w // 6
        e_y = h // 2 - e_height // 2
        
        cv2.rectangle(mask, (e_x, e_y), (e_x + e_width * 4, e_y + e_height), 255, -1)
        
        # 应用掩码
        result = base_image.copy()
        result[mask == 0] = 255  # 将非E区域设为白色
        
        return result
    
    def generate_size_error_small(self, base_image):
        """生成尺寸过小的样本"""
        scale_factor = random.uniform(0.2, 0.5)
        new_size = (int(self.base_size * scale_factor), int(self.base_size * scale_factor))
        resized = cv2.resize(base_image, new_size)
        
        # 将小图放在白色背景中央
        result = np.ones((self.base_size, self.base_size, 3), dtype=np.uint8) * 255
        y_offset = (self.base_size - new_size[1]) // 2
        x_offset = (self.base_size - new_size[0]) // 2
        result[y_offset:y_offset+new_size[1], x_offset:x_offset+new_size[0]] = resized
        
        return result
    
    def generate_size_error_large(self, base_image):
        """生成尺寸过大的样本（只显示部分）"""
        scale_factor = random.uniform(1.5, 2.5)
        new_size = (int(self.base_size * scale_factor), int(self.base_size * scale_factor))
        resized = cv2.resize(base_image, new_size)
        
        # 裁剪中心部分
        start_x = (new_size[0] - self.base_size) // 2
        start_y = (new_size[1] - self.base_size) // 2
        cropped = resized[start_y:start_y+self.base_size, start_x:start_x+self.base_size]
        
        return cropped
    
    def generate_ratio_error(self, base_image):
        """生成宽高比错误的样本"""
        # 随机选择是宽度错误还是高度错误
        if random.random() > 0.5:
            # 宽度错误
            new_width = int(self.base_size * random.uniform(0.5, 0.8))
            new_size = (new_width, self.base_size)
        else:
            # 高度错误
            new_height = int(self.base_size * random.uniform(0.5, 0.8))
            new_size = (self.base_size, new_height)
            
        resized = cv2.resize(base_image, new_size)
        
        # 放在白色背景中央
        result = np.ones((self.base_size, self.base_size, 3), dtype=np.uint8) * 255
        y_offset = (self.base_size - new_size[1]) // 2
        x_offset = (self.base_size - new_size[0]) // 2
        result[y_offset:y_offset+new_size[1], x_offset:x_offset+new_size[0]] = resized
        
        return result
    
    def generate_perspective_error(self, base_image):
        """生成透视变形样本"""
        h, w = base_image.shape[:2]
        
        # 定义原始四个角点
        pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
        
        # 随机生成透视变换后的四个角点
        max_offset = w // 4
        pts2 = np.float32([
            [random.randint(0, max_offset), random.randint(0, max_offset)],
            [w - random.randint(0, max_offset), random.randint(0, max_offset)],
            [random.randint(0, max_offset), h - random.randint(0, max_offset)],
            [w - random.randint(0, max_offset), h - random.randint(0, max_offset)]
        ])
        
        # 计算透视变换矩阵
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        
        # 应用透视变换
        result = cv2.warpPerspective(base_image, matrix, (w, h), borderValue=(255, 255, 255))
        
        return result
    
    def generate_distortion_error(self, base_image):
        """生成扭曲变形样本"""
        transform = A.Compose([
            A.GridDistortion(num_steps=5, distort_limit=0.3, p=1.0)
        ])
        
        result = transform(image=base_image)['image']
        return result
    
    def generate_rotation_error(self, base_image):
        """生成旋转错误样本"""
        angle = random.uniform(15, 75)  # 旋转15-75度
        
        h, w = base_image.shape[:2]
        center = (w // 2, h // 2)
        
        # 计算旋转矩阵
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # 应用旋转
        result = cv2.warpAffine(base_image, matrix, (w, h), flags=cv2.INTER_LINEAR, 
                               borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        
        return result
    
    def generate_blur_error(self, base_image):
        """生成模糊样本"""
        blur_amount = random.choice([3, 5, 7])  # 模糊核大小
        result = cv2.GaussianBlur(base_image, (blur_amount, blur_amount), 0)
        return result
    
    def generate_noise_error(self, base_image):
        """生成噪声样本"""
        # 添加高斯噪声
        noise = np.random.normal(0, 25, base_image.shape).astype(np.uint8)
        result = cv2.add(base_image, noise)
        
        # 确保值在有效范围内
        result = np.clip(result, 0, 255)
        
        return result
    
    def generate_stretch_error(self, base_image):
        """生成拉伸变形样本"""
        h, w = base_image.shape[:2]
        
        # 随机选择拉伸方向
        if random.random() > 0.5:
            # 水平拉伸
            new_width = int(w * random.uniform(1.2, 1.8))
            new_size = (new_width, h)
        else:
            # 垂直拉伸
            new_height = int(h * random.uniform(1.2, 1.8))
            new_size = (w, new_height)
            
        stretched = cv2.resize(base_image, new_size)
        
        # 裁剪回原始尺寸
        if stretched.shape[1] > w:  # 水平拉伸
            start_x = (stretched.shape[1] - w) // 2
            result = stretched[:, start_x:start_x+w]
        else:  # 垂直拉伸
            start_y = (stretched.shape[0] - h) // 2
            result = stretched[start_y:start_y+h, :]
            
        return result
    
    def generate_samples(self, num_samples_per_type=10):
        """为每种缺陷类型生成指定数量的样本"""
        print(f"开始生成不合格CE标志样本，每种类型{num_samples_per_type}个...")
        
        for i in range(num_samples_per_type):
            # 生成标准CE标志作为基础
            base_ce = self.create_standard_ce()
            
            # 为每种缺陷类型生成样本
            samples = {
                "partial_c": self.generate_partial_c(base_ce),
                "partial_e": self.generate_partial_e(base_ce),
                "size_error_small": self.generate_size_error_small(base_ce),
                "size_error_large": self.generate_size_error_large(base_ce),
                "ratio_error": self.generate_ratio_error(base_ce),
                "perspective_error": self.generate_perspective_error(base_ce),
                "distortion_error": self.generate_distortion_error(base_ce),
                "rotation_error": self.generate_rotation_error(base_ce),
                "blur_error": self.generate_blur_error(base_ce),
                "noise_error": self.generate_noise_error(base_ce),
                "stretch_error": self.generate_stretch_error(base_ce)
            }
            
            # 保存所有样本
            for defect_type, sample in samples.items():
                filename = os.path.join(self.output_path, defect_type, f"{defect_type}_{i:03d}.png")
                cv2.imwrite(filename, cv2.cvtColor(sample, cv2.COLOR_RGB2BGR))
        
        print(f"样本生成完成！已保存到: {self.output_path}")
        
        # 打印生成统计
        total_files = 0
        for defect_type in self.defect_types:
            count = len(os.listdir(os.path.join(self.output_path, defect_type)))
            total_files += count
            print(f"- {defect_type}: {count}个样本")
        
        print(f"总计生成: {total_files}个不合格样本")

# 使用示例
if __name__ == "__main__":
    # 设置输出路径
    output_directory = "./ce_defective_samples"
    
    # 创建生成器实例
    generator = CEDefectGenerator(output_directory)
    
    # 生成样本（每种类型10个）
    generator.generate_samples(num_samples_per_type=10)
    
    print("\n样本生成完成！您可以在以下目录中找到所有不合格CE标志样本：")
    print(output_directory)