# 最终优化版本 - 修复参数错误
from ultralytics import YOLO
import os
import time
import torch
import psutil
from datetime import datetime

# 设置环境变量，优化CPU性能
os.environ['OMP_NUM_THREADS'] = '10'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['KMP_AFFINITY'] = 'granularity=fine,compact,1,0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''

def set_cpu_optimization():
    """设置CPU优化配置"""
    try:
        # 设置CPU亲和性，绑定到性能核心
        p = psutil.Process()
        p.cpu_affinity([0, 1, 2, 3, 4, 5, 6, 7])
        print(f"已设置CPU亲和性，使用核心: {[0, 1, 2, 3, 4, 5, 6, 7]}")
    except Exception as e:
        print(f"设置CPU亲和性失败: {e}")
    
    # 设置PyTorch线程数
    torch.set_num_threads(10)
    print(f"PyTorch线程数: {torch.get_num_threads()}")

def set_high_priority():
    """设置进程高优先级"""
    try:
        p = psutil.Process()
        if hasattr(psutil, 'HIGH_PRIORITY_CLASS'):
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            print("已设置高进程优先级")
        else:
            p.nice(-10)
            print("已设置高进程优先级 (nice = -10)")
    except Exception as e:
        print(f"设置进程优先级失败: {e}")

# 应用CPU优化
set_cpu_optimization()
set_high_priority()

print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"CPU核心数: {os.cpu_count()}")
print(f"使用的CPU线程数: 10/12")
print(f"数据集大小: 1284张图片")
print(f"训练类别: 5类 (V-267A, Lion, CE_Mark, UKCA, C-267G)")

# 生成唯一项目名称
current_time = datetime.now().strftime("%m%d_%H%M")
project_name = f"detect_optimized_{current_time}"

# 加载模型
model = YOLO("yolo11s.pt")

# 训练配置 - 修复参数错误版本
model.train(
    data="yolo-Finalprocessing.yaml",
    epochs=200,
    patience=35,
    project="runs",
    name=project_name,
    exist_ok=False,
    batch=10,
    imgsz=640,
    device='cpu',
    workers=8,                    # 只保留支持的参数
    lr0=0.015,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3.0,
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    cos_lr=True,
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
    auto_augment='randaugment',
    val=True,
    plots=True,
    save=True,
    save_period=15,
    amp=False,
    single_cls=False,
    verbose=False,
    deterministic=True
)

print("训练完成！")
#輸出為：detect_optimized_