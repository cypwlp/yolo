# 最终优化版本 - 小目标检测专用CPU训练（不覆盖版本）
import os
import time
from datetime import datetime

import psutil
import torch

from ultralytics import YOLO

# 设置环境变量，优化CPU性能
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["CUDA_VISIBLE_DEVICES"] = ""


def set_cpu_affinity():
    """设置CPU亲和性，避免占用所有核心."""
    try:
        p = psutil.Process()
        p.cpu_affinity(list(range(0, 8)))
        print(f"已设置CPU亲和性，使用核心: {list(range(0, 8))}")
    except Exception as e:
        print(f"设置CPU亲和性失败: {e}")


# 应用CPU限制
set_cpu_affinity()
torch.set_num_threads(8)

print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"CPU核心数: {os.cpu_count()}")
print("使用的CPU核心数: 8/12")
print("数据集大小: 1284张图片")
print("训练类别: 5类 (V-267A, Lion, CE_Mark, UKCA, C-267G)")

# 生成唯一项目名称
current_time = datetime.now().strftime("%m%d_%H%M")
project_name = f"detect_train_{current_time}"

# 加载模型
model = YOLO("yolo11s.pt")

# 训练配置 - 关键修改：使用project和name参数
model.train(
    # 基础配置
    data="yolo-Finalprocessing.yaml",
    epochs=200,
    patience=35,
    # 重要：设置项目名称避免覆盖
    project="runs",  # 项目目录
    name=project_name,  # 唯一实验名称
    exist_ok=False,  # 设置为False，如果存在则报错
    # CPU多任务优化配置
    batch=6,
    imgsz=640,
    # 设备设置
    device="cpu",
    workers=3,
    # 优化器与学习率
    lr0=0.01,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3.0,
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    # 学习率调度
    cos_lr=True,
    # 数据增强
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=10.0,
    translate=0.1,
    scale=0.5,
    shear=2.0,
    perspective=0.001,
    fliplr=0.5,
    mosaic=1.0,
    mixup=0.15,
    copy_paste=0.0,
    erasing=0.4,
    auto_augment="randaugment",
    # 验证设置
    val=True,
    plots=True,
    save=True,
    save_period=10,
    # 其他优化
    amp=False,
    single_cls=False,
    verbose=True,
    deterministic=True,
)

print(f"训练完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"训练结果保存在: runs/detect/{project_name}")
print("训练完成！开始验证最佳模型...")

# 验证最佳模型 - 同样指定项目名称
model.val(
    data="yolo-Finalprocessing.yaml",
    project="runs",
    name=f"val_{project_name}",  # 验证结果也单独保存
    save_json=True,
    plots=True,
    conf=0.001,
    iou=0.6,
)

print("验证完成！")
print(f"所有结果都保存在: runs/detect/{project_name}")
print("下一步建议：")
print("1. 检查验证结果中的mAP指标")
print("2. 使用模型进行切片检测推理")
print("3. 如果小目标检测效果不佳，考虑增加更多小目标样本")
# 輸出為：detect_train_
