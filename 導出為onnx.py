# fix_yolo11_export_complete.py
from ultralytics import YOLO
import os
import shutil

def export_yolo11_fixed():
    """正确导出YOLOv11模型"""
    
    print("🔄 开始修复YOLOv11模型导出...")
    
    # 加载训练好的模型
    model_path = r"C:\Users\20250923\Desktop\ultralytics-main\runs\detect_optimized_1107_1657\weights\best.pt"
    model = YOLO(model_path)
    
    # 测试原始模型
    print("🧪 测试原始YOLOv11模型...")
    results = model.predict(r"C:\Users\20250923\Desktop\TestPNG\test21.png", save=True, conf=0.25, imgsz=640)
    
    for i, r in enumerate(results):
        print(f"📊 原始模型检测结果 {i+1}: {len(r.boxes)} 个目标")
        for j, box in enumerate(r.boxes):
            print(f"  目标 {j+1}: {model.names[int(box.cls)]}, 置信度: {box.conf.item():.3f}")
    
    # 导出为ONNX - 针对YOLOv11的特殊设置
    print("🔄 导出YOLOv11 ONNX模型...")
    export_result = model.export(
        format="onnx",
        opset=17,
        simplify=True,
        dynamic=False,
        imgsz=640,
        batch=1
    )
    
    print(f"✅ YOLOv11 ONNX模型导出完成: {export_result}")
    
    # 测试导出的ONNX模型
    print("🧪 测试ONNX模型...")
    onnx_model = YOLO(export_result)
    onnx_results = onnx_model.predict(r"C:\Users\20250923\Desktop\TestPNG\test21.png", save=True, conf=0.25)
    
    for i, r in enumerate(onnx_results):
        print(f"📊 ONNX模型检测结果 {i+1}: {len(r.boxes)} 个目标")
        for j, box in enumerate(r.boxes):
            print(f"  目标 {j+1}: {model.names[int(box.cls)]}, 置信度: {box.conf.item():.3f}")

    # 复制到目标目录
    target_dir = r"C:\Users\20250923\Desktop\YolovNewPorject\UserClient\StandaloneTargetDetectioClient\Models"
    target_path = os.path.join(target_dir, "yolo11s_optimized_fixed.onnx")
    
    shutil.copy2(export_result, target_path)
    print(f"✅ 模型已复制到: {target_path}")

if __name__ == "__main__":
    export_yolo11_fixed()