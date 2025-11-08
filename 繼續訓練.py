# 如果您想继续训练
model = YOLO(r"C:\Users\20250923\Desktop\ultralytics-main\runs\detect_optimized_1107_1657\weights\last.pt")
model.train(
    resume=True,  # 继续训练
    epochs=150,   # 总epochs
    patience=50,  # 增加耐心值
    plots=True    # 生成完整图表
)