"""
================================================================================
完整几何动力学方程 (Complete Geometric Dynamical Equation)
================================================================================

本文件包含两个版本的动力学方程，用于不同的研究目的。

================================================================================
版本一：完整几何动力学方程 (Zero-Parameter Geometric Equation)
================================================================================
功能: 零自由参数。所有参数由60°不变性、圆锥几何、零点密度严格导出。
      比值 r(t) = 2√3 / log(t/2π) 为对数衰减函数，由密度-螺距匹配确定。
      支持正向零点(正半平面)和负向零点(负半平面)，运算级对称。
      输出完整预测结果到 XLSX 文件。

完整方程 (Final Zero-Parameter Equation):
  t_n = 2*t_{n-1} - t_{n-2} + π/√3 - (log(t_{n-1}/2π) / (2√3)) * (t_{n-1} - t_{n-2})

参数来源 (Parameter Sources):
  系数2 = sec60° = 1/cos60° (几何锁定, geometrically locked)
  c₂ = π/√3 = π·cot60° (垂直势梯度常数, potential gradient constant)
  β = 1/4 (几何耦合常数, brachistochrone principle on cone)
  dC/dh = 4π/√3 (截面周长变化率, circumference rate of change)
  r(t) = 2√3 / log(t/2π) (密度-螺距匹配, density-pitch matching)
  无任何自由参数 (Zero free parameters).

垂直势函数 (Vertical Potential):
  Φ(t) = -(π/√3)·t (线性势, linear potential)
  Φ'(t) = -π/√3 (常数势梯度, constant potential gradient)

理论依据 (References):
  Section 8.6: Density-Pitch Matching → r(t) = 2√3 / log(t/2π)
  Section 8.2: Brachistochrone Principle → β = 1/4
  Section 8.1: Geometric Constraint → Φ'(t) = -c₂ (constant)
  Section 8.7: Final Zero-Parameter Equation
  Section 10.1: Rigorous Derivation of the 5^m Cycle
  Section 12: Geometric Equivalence — Framework as the Critical Line

================================================================================
版本二：参数动力学方程 (Parameterized Fitted Equation)
================================================================================
功能: 早期数值拟合阶段使用的参数化版本，用于验证理论方向和对比基准。
      参数 m 和 γ 通过训练集拟合得到，不属于几何导出常数。
      此版本保留用于：
      (1) 历史对比：展示几何版 vs 拟合版的精度提升
      (2) 方法验证：证明几何版的零自由参数优越性

参数化方程:
  t_n = 2*t_{n-1} - t_{n-2} - (1/m)(Φ'(t_{n-1}) + γ*(t_{n-1} - t_{n-2}))

注意:
  - 这些拟合参数仅作为历史记录保留，不进入最终理论公式。
  - 根据论文 Section 7 的数值验证，完整几何方程（零自由参数）在所有
    训练配置上均优于参数拟合版本，在 100,000 零点上 RMSE 降低 38.4%。

================================================================================
负向零点对称性 (Negative Zero Symmetry) — 适用于两个版本
================================================================================
  正向: 零点递增, 力向上
  负向: 零点递减, 力向下 (整体反号)
  RMSE 完全一致 (运算级对称)

数据: LMFDB 黎曼zeta函数非平凡零点虚部
================================================================================
"""

import numpy as np
import pandas as pd

# ==================== 配置 ====================
DATA_FILE = r"D:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_100000.npy"
OUTPUT_XLSX = r"D:\60_Degree_Invariant_Riemann_Hypothesis\perfect_form_results.xlsx"

# ==================== 几何常数（零自由参数）====================
COEFF_2 = 2.0                           # sec60° = 1/cos60°
C2 = np.pi / np.sqrt(3)                 # π/√3 = π·cot60°
PI_OVER_SQRT3 = np.pi / np.sqrt(3)      # π/√3 (常数驱动项)
TWO_SQRT3 = 2 * np.sqrt(3)              # 2√3
TWO_PI = 2 * np.pi                      # 2π

print("=" * 80)
print("完整几何动力学方程验证 - Complete Geometric Dynamical Equation")
print("=" * 80)
print(f"系数2 = {COEFF_2} (几何: sec60° = 1/cos60°)")
print(f"c₂ = π/√3 = {C2:.10f} (垂直势梯度常数, π·cot60°)")
print(f"r(t) = 2√3 / log(t/2π) (对数衰减比值函数, 密度-螺距匹配)")
print(f"推力项 = π/√3 = {PI_OVER_SQRT3:.6f}")
print(f"零自由参数 - Zero Free Parameters")
print()

# ==================== 加载数据 ====================
t_all = np.load(DATA_FILE)
total = len(t_all)

print(f"加载 {total} 个零点")
print(f"t 范围: {t_all[0]:.2f} ~ {t_all[-1]:.2f}")
print()

# ==================== 预测函数（直接使用最终零参数方程）====================
def predict_geometric(t_seq, phi_sign=1):
    """完整几何动力学方程预测（零自由参数，m 不参与任何运算）
    
    直接使用论文最终方程:
    t_n = 2*t_{n-1} - t_{n-2} + π/√3 
          - (log(t_{n-1}/2π) / (2√3)) * (t_{n-1} - t_{n-2})
    
    phi_sign: 1 用于正向零点, -1 用于负向零点（力的方向反转）
    """
    n = len(t_seq)
    preds = []
    acts = []
    
    for i in range(2, n):
        t_prev = t_seq[i-1]
        t_prev2 = t_seq[i-2]
        t_actual = t_seq[i]
        
        # 对数衰减系数
        log_term = np.log(np.maximum(t_prev, TWO_PI + 1e-10) / TWO_PI)
        damping_coeff = log_term / TWO_SQRT3
        
        # 完整零参数方程（m 不在任何地方出现）
        pred = (COEFF_2 * t_prev 
                - t_prev2 
                + phi_sign * PI_OVER_SQRT3 
                - phi_sign * damping_coeff * (t_prev - t_prev2))
        
        preds.append(pred)
        acts.append(t_actual)
    
    return np.array(preds), np.array(acts)


# ==================== 评估函数 ====================
def evaluate(preds, acts, label):
    """评估预测精度"""
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(np.abs(acts)) * 100
    avg_spacing = np.mean(np.abs(np.diff(acts)))
    max_err = np.max(np.abs(errors))
    min_err = np.min(np.abs(errors))
    
    print(f"\n{label}:")
    print(f"  预测数量: {len(preds)}")
    print(f"  RMSE = {rmse:.8f}")
    print(f"  MAE = {mae:.8f}")
    print(f"  相对误差 = {rel_err:.8f}%")
    print(f"  平均零点间距 = {avg_spacing:.4f}")
    print(f"  绝对误差范围: [{min_err:.8f}, {max_err:.8f}]")
    
    return rmse, mae, rel_err


# ==================== 正向零点全序列验证（完整几何版）====================
print("=" * 80)
print("正向零点验证 — 完整几何方程 (Positive Zeros — Geometric Equation)")
print("=" * 80)

preds_geo, acts_geo = predict_geometric(t_all, phi_sign=1)
rmse_geo, mae_geo, rel_geo = evaluate(preds_geo, acts_geo, "完整几何方程 (零自由参数)")

# ==================== 打印前100个预测结果 ====================
print()
print("=" * 100)
print("前100个零点预测结果")
print("=" * 100)
print(f"{'n':<8} {'t实际':<18} {'t预测':<18} {'绝对误差':<16} {'相对误差%':<14}")
print("-" * 80)
indices = np.arange(3, total + 1)
abs_errors_geo = np.abs(acts_geo - preds_geo)
rel_errors_geo = abs_errors_geo / acts_geo * 100

for i in range(min(100, len(preds_geo))):
    print(f"{indices[i]:<8} {acts_geo[i]:<18.8f} {preds_geo[i]:<18.8f} "
          f"{abs_errors_geo[i]:<16.8f} {rel_errors_geo[i]:<14.8f}")

print(f"... (共 {len(preds_geo)} 个) ...")

# ==================== 打印最后10个预测结果 ====================
print()
print("=" * 100)
print("最后10个零点预测结果")
print("=" * 100)
print(f"{'n':<8} {'t实际':<18} {'t预测':<18} {'绝对误差':<16} {'相对误差%':<14}")
print("-" * 80)

for i in range(len(preds_geo)-10, len(preds_geo)):
    print(f"{indices[i]:<8} {acts_geo[i]:<18.8f} {preds_geo[i]:<18.8f} "
          f"{abs_errors_geo[i]:<16.8f} {rel_errors_geo[i]:<14.8f}")

# ==================== 逐段误差分析 ====================
print()
print("=" * 100)
print("逐500个零点误差分析")
print("=" * 100)
print(f"{'零点范围':<16} {'RMSE':<14} {'MAE':<14} {'相对误差%':<14}")
print("-" * 65)

for start in range(2, total, 500):
    end = min(start + 500, total)
    seg_preds = []
    seg_acts = []
    
    for i in range(start, end):
        t_prev = t_all[i-1]
        t_prev2 = t_all[i-2]
        
        log_term = np.log(np.maximum(t_prev, TWO_PI + 1e-10) / TWO_PI)
        damping_coeff = log_term / TWO_SQRT3
        
        pred = (COEFF_2 * t_prev 
                - t_prev2 
                + PI_OVER_SQRT3 
                - damping_coeff * (t_prev - t_prev2))
        
        seg_preds.append(pred)
        seg_acts.append(t_all[i])
    
    seg_preds = np.array(seg_preds)
    seg_acts = np.array(seg_acts)
    seg_errors = seg_acts - seg_preds
    seg_rmse = np.sqrt(np.mean(seg_errors**2))
    seg_mae = np.mean(np.abs(seg_errors))
    seg_rel = seg_mae / np.mean(seg_acts) * 100
    
    print(f"t_{start}-t_{end:<5} {seg_rmse:<14.8f} {seg_mae:<14.8f} {seg_rel:<14.8f}")

# ==================== 负向零点验证（对称性检验）====================
print()
print("=" * 80)
print("负向零点验证 — 对称性检验 (Negative Zeros — Symmetry Check)")
print("=" * 80)

t_negative = -t_all
preds_neg, acts_neg = predict_geometric(t_negative, phi_sign=-1)
rmse_neg, mae_neg, rel_neg = evaluate(preds_neg, acts_neg, "负向零点 (完整几何方程)")

print()
print("=" * 80)
print("对称性检验结果")
print("=" * 80)
print(f"正向 RMSE = {rmse_geo:.8f}, 负向 RMSE = {rmse_neg:.8f}")
if abs(rmse_geo - rmse_neg) < 1e-6:
    print("★ 正向与负向 RMSE 完全一致，运算级对称性验证通过。")
else:
    print(f"差异: {abs(rmse_geo - rmse_neg):.10f}")

# ==================== 对比：旧版固定 γ（参数拟合历史版本）====================
print()
print("=" * 80)
print("对比：完整几何方程 vs 旧版固定 γ（参数拟合历史版本）")
print("=" * 80)

gamma_old = 0.001605
m_old = 0.001
c2_old = m_old * np.pi / np.sqrt(3)  # 注意：旧版用此值，但 m 在代数中会被消去

preds_old = []
for i in range(2, total):
    t_prev = t_all[i-1]
    t_prev2 = t_all[i-2]
    phi_prime = -c2_old
    pred = (COEFF_2 * t_prev 
            - t_prev2 
            - (1/m_old) * (phi_prime + gamma_old * (t_prev - t_prev2)))
    preds_old.append(pred)
preds_old = np.array(preds_old)
rmse_old = np.sqrt(np.mean((t_all[2:] - preds_old)**2))
mae_old = np.mean(np.abs(t_all[2:] - preds_old))
rel_old = mae_old / np.mean(t_all[2:]) * 100

print(f"\n旧版固定 γ=0.001605 (参数拟合版):")
print(f"  RMSE = {rmse_old:.8f}")
print(f"  MAE = {mae_old:.8f}")
print(f"  相对误差 = {rel_old:.8f}%")

print(f"\n完整几何版 (零自由参数, m 已消除):")
print(f"  RMSE = {rmse_geo:.8f}")
print(f"  MAE = {mae_geo:.8f}")
print(f"  相对误差 = {rel_geo:.8f}%")

improvement = (rmse_old - rmse_geo) / rmse_old * 100
print(f"\n★ 完整几何版 RMSE 降低 {improvement:.1f}%")

# ==================== 输出到 XLSX ====================
df = pd.DataFrame({
    'n': indices,
    't_actual': acts_geo,
    't_predicted': preds_geo,
    'abs_error': abs_errors_geo,
    'rel_error_%': rel_errors_geo,
    't_{n-1}': t_all[1:-1],
    'velocity': np.diff(t_all[:-1])
})

stats_data = {
    '指标': ['RMSE (几何版)', 'MAE (几何版)', '相对误差% (几何版)',
            'RMSE (旧版固定γ)', 'MAE (旧版固定γ)', '相对误差% (旧版固定γ)',
            'RMSE提升%', '平均零点间距', '预测数量', '数据文件'],
    '值': [rmse_geo, mae_geo, rel_geo,
           rmse_old, mae_old, rel_old,
           improvement, np.mean(np.abs(np.diff(acts_geo))), len(preds_geo), DATA_FILE]
}
df_stats = pd.DataFrame(stats_data)

with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='预测结果', index=False)
    df_stats.to_excel(writer, sheet_name='统计汇总', index=False)

print(f"\n完整结果已保存到: {OUTPUT_XLSX}")
print(f"  - Sheet '预测结果': {len(df)} 行，包含所有预测值和误差")
print(f"  - Sheet '统计汇总': 汇总统计指标（含几何版vs旧版固定γ对比）")

# ==================== 总结 ====================
print()
print("=" * 80)
print("完整几何动力学方程")
print("=" * 80)
print(f"t_n = 2*t_{{n-1}} - t_{{n-2}} + π/√3")
print(f"      - (log(t_{{n-1}}/2π) / (2√3)) * (t_{{n-1}} - t_{{n-2}})")
print(f"")
print(f"所有参数由60°不变性和圆锥几何锁定，m 已从理论公式中完全消除。")
print(f"All parameters geometrically locked. m eliminated from theoretical formula.")
print(f"")
print(f"理论依据: Section 8.7, 10.1, 12")
print(f"数值验证: 100,000 零点, 相对误差 {rel_geo:.6f}%")
print(f"结果文件: {OUTPUT_XLSX}")
print()
print("完成 (Done)!")