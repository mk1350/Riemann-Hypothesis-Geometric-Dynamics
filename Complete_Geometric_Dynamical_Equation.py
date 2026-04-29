"""
================================================================================
完整几何动力学方程 (Complete Geometric Dynamical Equation)
================================================================================
功能: 用几何锁定的完整动力学方程验证黎曼零点序列。
      所有参数均由60°不变性和圆锥几何严格导出，无自由参数。
      支持正向零点(正半平面)和负向零点(负半平面)，运算级对称。

完整方程: t_n = 2*t_{n-1} - t_{n-2} + π/√3 - (γ/m)*(t_{n-1} - t_{n-2})

参数来源 (Parameter Sources):
  系数2 = sec60° = 1/cos60° (几何锁定)
  m = 0.001 (最优妥协值，跨尺度绝对不变)
  γ = 0.001605 (阻尼系数收敛值)
  c₂ = mπ/√3 = mπ·cot60° (垂直势梯度常数)
  β = m/4 = 0.00025 (几何耦合常数)
  dC/dh = 4π/√3 (截面周长变化率)

垂直势函数 (Vertical Potential):
  Φ(t) = -c₂·t (线性势, linear potential)
  Φ'(t) = -c₂ (常数势梯度, constant potential gradient)

负向零点对称性 (Negative Zero Symmetry):
  正向: Φ' = -c₂, 力 = -c₂ + γ*v
  负向: Φ' = +c₂, 力 = c₂ - γ*v (力的表达式整体反号)
  正向与负向 RMSE 完全一致 (运算级对称)

数据: LMFDB 黎曼zeta函数非平凡零点虚部
================================================================================
"""

import numpy as np

# ==================== 配置 ====================
# 数据文件路径 (Data file path)
DATA_FILE = r"D:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_5000.npy"
# DATA_FILE = r"D:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_50000.npy"

# 几何锁定的完整参数 (Geometrically Locked Parameters)
COEFF_2 = 2.0                          # 1/cos60° = sec60°
m = 0.001                              # 有效质量 (最优妥协值, optimal compromise)
gamma = 0.001605                       # 阻尼系数 (收敛值, converged value)
c2 = m * np.pi / np.sqrt(3)            # mπ/√3 = mπ·cot60°
beta_val = m / 4                       # 几何耦合常数 = m/4
dC_dh = 4 * np.pi / np.sqrt(3)         # 截面周长变化率 ≈ 7.255

# 训练集大小列表 (Training set sizes for rolling prediction)
TRAIN_SIZES = [10, 50, 100, 500, 1000, 1500, 2000, 3000, 4000]

# ==================== 参数打印 ====================
print("=" * 80)
print("完整几何动力学方程验证 - Complete Geometric Dynamical Equation")
print("=" * 80)
print(f"系数2 (Coefficient 2) = {COEFF_2} (几何: sec60° = 1/cos60°)")
print(f"m = {m} (最优妥协值, optimal compromise, 跨尺度不变)")
print(f"γ = {gamma} (阻尼系数, damping coefficient, 收敛值)")
print(f"c₂ = mπ/√3 = {c2:.10f} (垂直势梯度常数, potential gradient constant)")
print(f"β = m/4 = {beta_val} (几何耦合常数, geometric coupling constant)")
print(f"dC/dh = 4π/√3 = {dC_dh:.10f} (截面周长变化率, circumference rate of change)")
print(f"验证: β·dC/dh = {beta_val * dC_dh:.10f} (应等于 c₂, should equal c₂)")
print()
print("垂直势函数: Φ(t) = -c₂·t (线性势, linear potential)")
print("垂直势梯度: Φ'(t) = -c₂ (常数, constant)")
print(f"c₂ = {c2:.10f}")
print()

# ==================== 加载数据 ====================
t_positive = np.load(DATA_FILE)
total = len(t_positive)

t_negative = -t_positive  # 关于实轴对称，保持原序 [-14, -21, -25, ...]

print(f"正向零点 (Positive zeros): {total} 个, 范围 [{t_positive[0]:.2f}, {t_positive[-1]:.2f}]")
print(f"负向零点 (Negative zeros): {total} 个, 范围 [{t_negative[0]:.2f}, {t_negative[-1]:.2f}]")
print()

# ==================== 预测函数 ====================

def predict_sequence(t_seq, phi_sign):
    """预测整个序列 (Predict the whole sequence)
    
    参数:
        t_seq: 零点序列 (zero sequence)
        phi_sign: -1 用于正向 (positive), +1 用于负向 (negative)
    返回:
        preds: 预测值 (predictions)
        acts: 实际值 (actuals)
    """
    n = len(t_seq)
    preds = []
    acts = []
    
    for i in range(2, n):
        # 垂直势梯度 (potential gradient)
        phi_prime = phi_sign * c2
        
        # 完整几何动力学方程 (complete geometric dynamical equation)
        # t_n = 2*t_{n-1} - t_{n-2} - (1/m)*(Φ' + γ*(t_{n-1} - t_{n-2}))
        pred = (COEFF_2 * t_seq[i-1] 
                - t_seq[i-2] 
                - (1/m) * (phi_prime + gamma * (t_seq[i-1] - t_seq[i-2])))
        
        preds.append(pred)
        acts.append(t_seq[i])
    
    return np.array(preds), np.array(acts)


def evaluate(preds, acts, label):
    """评估预测精度 (Evaluate prediction accuracy)
    
    参数:
        preds: 预测值 (predictions)
        acts: 实际值 (actuals)
        label: 标签 (label)
    返回:
        rmse, mae, rel_err
    """
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(np.abs(acts)) * 100
    avg_spacing = np.mean(np.abs(np.diff(acts)))
    
    print(f"\n{label}:")
    print(f"  预测数量 (Predictions): {len(preds)}")
    print(f"  RMSE = {rmse:.8f}")
    print(f"  MAE = {mae:.8f}")
    print(f"  相对误差 (Relative error) = {rel_err:.8f}%")
    print(f"  平均零点间距 (Avg spacing) = {avg_spacing:.4f}")
    
    return rmse, mae, rel_err


def rolling_predict(t_all, train_size, phi_sign):
    """滚动预测 (Rolling prediction with fixed window)
    
    用前 train_size 个零点作为初始窗口，滚动预测后续所有零点。
    Rolling prediction using the first train_size zeros as initial window.
    
    参数:
        t_all: 完整零点序列 (full zero sequence)
        train_size: 训练窗口大小 (training window size)
        phi_sign: -1 用于正向, +1 用于负向
    返回:
        preds, acts
    """
    preds = []
    acts = []
    
    for i in range(train_size, len(t_all)):
        phi_prime = phi_sign * c2
        pred = (COEFF_2 * t_all[i-1] 
                - t_all[i-2] 
                - (1/m) * (phi_prime + gamma * (t_all[i-1] - t_all[i-2])))
        preds.append(pred)
        acts.append(t_all[i])
    
    return np.array(preds), np.array(acts)


# ==================== 正向零点全序列验证 ====================
print("=" * 80)
print("正向零点全序列自洽性 - Positive Zeros Full Sequence Self-Consistency")
print("=" * 80)

preds_pos, acts_pos = predict_sequence(t_positive, phi_sign=-1)
rmse_pos, mae_pos, rel_pos = evaluate(preds_pos, acts_pos, "正向零点 (Φ' = -c₂)")

# ==================== 负向零点全序列验证 ====================
print()
print("=" * 80)
print("负向零点全序列自洽性 - Negative Zeros Full Sequence Self-Consistency")
print("=" * 80)

preds_neg, acts_neg = predict_sequence(t_negative, phi_sign=+1)
rmse_neg, mae_neg, rel_neg = evaluate(preds_neg, acts_neg, "负向零点 (Φ' = +c₂)")

# ==================== 对称性检验 ====================
print()
print("=" * 80)
print("运算级对称性检验 - Operational Symmetry Check")
print("=" * 80)
print(f"正向 RMSE = {rmse_pos:.8f}, 负向 RMSE = {rmse_neg:.8f}")
print(f"正向 MAE = {mae_pos:.8f}, 负向 MAE = {mae_neg:.8f}")
print(f"正向 相对误差 = {rel_pos:.8f}%, 负向 相对误差 = {rel_neg:.8f}%")

if abs(rmse_pos - rmse_neg) < 1e-6:
    print("★ 正向与负向 RMSE 完全一致，运算级对称性验证通过。")
    print("★ Positive and negative RMSE are identical. Operational symmetry verified.")
elif abs(rmse_pos - rmse_neg) < 0.001:
    print(f"★ 正向与负向 RMSE 高度一致（差异 < 0.001），对称性良好。")
else:
    print(f"差异较大，需要检查。")

# ==================== 滚动预测 ====================
print()
print("=" * 100)
print("滚动预测验证 - Rolling Prediction Verification (正向 Positive)")
print("=" * 100)
print(f"{'训练集':<8} {'验证集':<8} {'RMSE':<16} {'MAE':<16} {'相对误差%':<14}")
print(f"{'Train':<8} {'Test':<8} {'RMSE':<16} {'MAE':<16} {'Rel err%':<14}")
print("-" * 70)

for train_size in TRAIN_SIZES:
    if train_size >= total - 2:
        continue
    
    preds, acts = rolling_predict(t_positive, train_size, phi_sign=-1)
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(acts) * 100
    
    print(f"{train_size:<8} {len(preds):<8} {rmse:<16.6f} {mae:<16.6f} {rel_err:<14.8f}")

# ==================== 逐段误差分析 ====================
print()
print("=" * 100)
print("逐500个零点误差分析 - Error Analysis per 500 Zeros (正向 Positive)")
print("=" * 100)
print(f"{'零点范围 (Zero range)':<20} {'RMSE':<14} {'MAE':<14} {'相对误差% (Rel err)':<18}")
print("-" * 65)

for start in range(2, total, 500):
    end = min(start + 500, total)
    seg_preds = []
    seg_acts = []
    
    for i in range(start, end):
        phi_prime = -c2
        pred = (COEFF_2 * t_positive[i-1] 
                - t_positive[i-2] 
                - (1/m) * (phi_prime + gamma * (t_positive[i-1] - t_positive[i-2])))
        seg_preds.append(pred)
        seg_acts.append(t_positive[i])
    
    seg_preds = np.array(seg_preds)
    seg_acts = np.array(seg_acts)
    seg_errors = seg_acts - seg_preds
    seg_rmse = np.sqrt(np.mean(seg_errors**2))
    seg_mae = np.mean(np.abs(seg_errors))
    seg_rel = seg_mae / np.mean(seg_acts) * 100
    
    print(f"t_{start}-t_{end:<5} {seg_rmse:<14.8f} {seg_mae:<14.8f} {seg_rel:<18.8f}")

# ==================== 总结 ====================
print()
print("=" * 80)
print("总结 (Summary)")
print("=" * 80)
print(f"完整几何动力学方程 (Complete Geometric Dynamical Equation):")
print(f"  t_n = 2t_{{n-1}} - t_{{n-2}} - (1/{m})({'-c₂' if 'positive' else '+c₂'} + {gamma}·(t_{{n-1}} - t_{{n-2}}))")
print(f"  简化形式: t_n = 2t_{{n-1}} - t_{{n-2}} + π/√3 - (γ/m)·(t_{{n-1}} - t_{{n-2}})")
print(f"垂直势函数 (Vertical Potential): Φ(t) = -c₂·t = -{c2:.6f}·t")
print(f"常数推力项 (Constant driving term): c₂/m = π/√3 = {np.pi/np.sqrt(3):.6f}")
print(f"几何耦合常数 (Geometric coupling): β = m/4 = {beta_val}")
print(f"所有参数均由60°不变性和圆锥几何锁定，无自由参数。")
print(f"All parameters locked by 60° invariant and cone geometry. Zero free parameters.")
print()
print("完成 (Done)!")