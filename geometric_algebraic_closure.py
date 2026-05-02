import numpy as np

# ==================== 几何公式 ====================
def S(h):
    return (2 * np.pi / np.sqrt(3)) * h**2

def V(h):
    return (4 * np.pi / 9) * h**3

def r_function(t):
    """对数衰减比值函数 r(t) = 2√3 / log(t/2π)"""
    t_safe = np.maximum(t, 2*np.pi + 1e-10)
    return 2 * np.sqrt(3) / np.log(t_safe / (2 * np.pi))

# ==================== 加载数据 ====================
DATA_FILE = r"F:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_100000.npy"
t_all = np.load(DATA_FILE)
total = len(t_all)

# 零回点
zero_return_indices = [2, 7, 32, 157, 782, 3907, 19532]

print("=" * 100)
print("S_V_5 验证闭环 — 引入 r(t) 作为几何-代数的转换函数")
print("=" * 100)

# ==================== 验证1：ΔV/ΔS 是否趋近 h？ ====================
print()
print("【验证1】ΔV/ΔS 与 h 的关系（理论：ΔV/ΔS ∝ h）")
print("-" * 80)
print(f"{'层间':<10} {'ΔV/ΔS':<18} {'h_mid':<18} {'(ΔV/ΔS)/h_mid':<20}")
print("-" * 70)

for i in range(len(zero_return_indices)-1):
    k1 = zero_return_indices[i]
    k2 = zero_return_indices[i+1]
    if k2 > total:
        break
    
    h1 = t_all[k1-1]
    h2 = t_all[k2-1]
    
    dS = S(h2) - S(h1)
    dV = V(h2) - V(h1)
    ratio = dV / dS
    h_mid = (h1 + h2) / 2
    normalized = ratio / h_mid
    
    print(f"m={i+1}→{i+2}:  {ratio:<18.6f} {h_mid:<18.6f} {normalized:<20.8f}")

# ==================== 验证2：ΔS 的增长因子 vs 5^{2/3} ====================
print()
print("【验证2】ΔS 的增长因子是否收敛到 5^{2/3} ≈ 2.924")
print("-" * 80)
print(f"{'层间':<10} {'ΔS增长因子':<16} {'5^{2/3}':<12} {'比值':<12}")
print("-" * 55)

dS_values = []
for i in range(len(zero_return_indices)-1):
    k1 = zero_return_indices[i]
    k2 = zero_return_indices[i+1]
    if k2 > total:
        break
    dS_values.append(S(t_all[k2-1]) - S(t_all[k1-1]))

target_ratio = 5 ** (2/3)  # ≈ 2.924

for i in range(1, len(dS_values)):
    growth = dS_values[i] / dS_values[i-1]
    ratio_to_target = growth / target_ratio
    print(f"m={i+1}→{i+2}:  {growth:<16.6f} {target_ratio:<12.6f} {ratio_to_target:<12.6f}")

print(f"\n理论收敛值: 5^(2/3) = {target_ratio:.6f}")

# ==================== 验证3：ΔV/(层内零点数 × r(t)) 是否为常数 ====================
print()
print("【验证3】核心假设：ΔV / (Δk × r) = 常数？")
print("  理论：ΔV ∝ h³, 层内零点数 Δk = 5^m, r(t) = 2√3/log(t/2π)")
print("  如果 ΔV 被 r(t) 和 Δk 共同约束，则三者比值应为常数")
print("-" * 100)
print(f"{'m':<6} {'Δk':<10} {'h_mid':<16} {'r(h_mid)':<14} {'ΔV':<18} {'ΔV/(Δk×r)':<20}")
print("-" * 90)

prev_h = None
prev_V_val = None

for m_idx, k in enumerate(zero_return_indices):
    if k > total:
        break
    
    m = m_idx + 1
    h = t_all[k-1]
    V_k = V(h)
    
    if m_idx == 0:
        prev_h = h
        prev_V_val = V_k
        continue
    
    dV_val = V_k - prev_V_val
    
    # 层内零点数
    if m_idx < len(zero_return_indices) - 1:
        dk = zero_return_indices[m_idx] - zero_return_indices[m_idx-1]
    else:
        dk = total - zero_return_indices[m_idx-1]
    
    h_mid = (prev_h + h) / 2
    r_mid = r_function(h_mid)
    
    ratio = dV_val / (dk * r_mid)
    
    print(f"{m:<6} {dk:<10} {h_mid:<16.2f} {r_mid:<14.6f} {dV_val:<18.6e} {ratio:<20.6e}")
    
    prev_h = h
    prev_V_val = V_k

# ==================== 验证4：S的增长指数是否稳定 ====================
print()
print("【验证4】S 环比的对数增长率")
print("-" * 60)
print(f"{'层间':<10} {'S环比':<14} {'log5(S环比)':<16} {'趋近于?':<10}")
print("-" * 55)

S_values = []
for k in zero_return_indices:
    if k <= total:
        S_values.append(S(t_all[k-1]))

for i in range(1, len(S_values)):
    ratio = S_values[i] / S_values[i-1]
    log5_ratio = np.log(ratio) / np.log(5)
    print(f"m={i}→{i+1}:  {ratio:<14.6f} {log5_ratio:<16.6f} {'→ 2?' if abs(log5_ratio-2)<0.3 else ''}")

print(f"\n理论预测：S ∝ h²，若 h 环比趋近 5^{1/3}，则 S 环比趋近 5^{2/3} ≈ 2.924")

# ==================== 总结 ====================
print()
print("=" * 100)
print("验证闭环总结")
print("=" * 100)
print("""
如果以下条件全部成立：
  1. ΔV/ΔS ∝ h（几何必然，已验证）
  2. ΔS 增长因子收敛到 5^{2/3}（引入 r(t) 后的预测）
  3. ΔV/(Δk × r(t)) = 常数（核心假设）
  
则证明：
  - S(h) 和 V(h) 是 5^m 周期结构的几何载体
  - r(t) 是连接几何（V, S）与代数（5）的转换函数
  - 整个系统的零自由参数闭环：几何 → r(t) → 代数周期 → 几何
""")

print("完成！")