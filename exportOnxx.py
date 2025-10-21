from ultralytics import YOLO
import os
import shutil
import onnx

# === 配置部分
model_list = [
    {
        "path": r"C:\Users\20250923\Desktop\ultralytics-main\runs\detect\train3\weights\best.pt",
        "name": "train3"
    },
    {
        "path": r"C:\Users\20250923\Desktop\ultralytics-main\runs\detect\train5\weights\best.pt",
        "name": "train5"
    }
]
export_dir = r"C:\Users\20250923\Desktop\项目\yolov8\CE_Mark_Test\CE_Mark_Test\Models"
# ============================

os.makedirs(export_dir, exist_ok=True)

for m in model_list:
    print(f"🚀 正在导出：{m['name']} ...")
    
    model = YOLO(m["path"])
    
    try:
        # 导出包含NMS的模型（推荐）
        export_result = model.export(
            format="onnx",  # 修正拼写错误
            opset=17,
            simplify=True,
            nms=True,       # 包含NMS，输出格式为 [1, num_detections, 6]
            dynamic=False
        )
        
        exported_path = str(export_result)
        if os.path.exists(exported_path):
            final_path = os.path.join(export_dir, f"{m['name']}.onnx")
            shutil.move(exported_path, final_path)
            print(f"✅ 导出成功：{final_path}")
            
            # 验证模型输出
            onnx_model = onnx.load(final_path)
            print(f"📊 {m['name']} 模型输出信息：")
            for i, output in enumerate(onnx_model.graph.output):
                print(f"  输出 {i}: 名称={output.name}, 形状={[dim.dim_value for dim in output.type.tensor_type.shape.dim]}")
                
        else:
            print(f"❌ 未找到导出文件：{exported_path}")
            
    except Exception as e:
        print(f"❌ 导出失败：{e}")
        import traceback
        traceback.print_exc()
        continue

print("🎯 所有模型导出完成！")