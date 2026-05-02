import numpy as np

# ==================== 配置 ====================
DATA_FILE = r"F:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_50000.npy"

# 几何常数
R_RATIO = 2 / np.sqrt(3)  # r(h) = 2h/√3

# 侧面积 S(h) = (2π/√3) * h²
def S(h):
    return (2 * np.pi / np.sqrt(3)) * h**2

# 体积 V(h) = (4π/9) * h³
def V(h):
    return (4 * np.pi / 9) * h**3

# ==================== 加载数据 ====================
t_all = np.load(DATA_FILE)
total = len(t_all)

# 零回点 k_m = (5^m + 3)/4
# k = 2, 7, 32, 157, 782, 3907, 19532...
zero_return_indices = [2, 7, 32, 157, 782, 3907, 19532]

print("=" * 100)
print("零回点处的 S(h) 和 V(h) 分析")
print("=" * 100)
print(f"几何公式:")
print(f"  S(h) = (2π/√3)·h² = {2*np.pi/np.sqrt(3):.6f}·h²")
print(f"  V(h) = (4π/9)·h³ = {4*np.pi/9:.6f}·h³")
print()

# ==================== 计算零回点处的 S 和 V ====================
print("=" * 120)
print(f"{'m':<6} {'k_m':<8} {'t_k':<18} {'S(t_k)':<18} {'V(t_k)':<20} {'ΔS':<18} {'ΔV':<20} {'ΔS比值':<14} {'ΔV比值':<14}")
print("-" * 120)

prev_S = None
prev_V = None
prev_dS = None
prev_dV = None

for m_idx, k in enumerate(zero_return_indices):
    if k > total:
        print(f"\n(零回点 k={k} 超出数据范围)")
        break
    
    m = m_idx + 1  # m从1开始
    t_k = t_all[k-1]  # k是1-based序号
    S_k = S(t_k)
    V_k = V(t_k)
    
    # 与上一个零回点的增量
    if prev_S is not None:
        dS = S_k - prev_S
        dV = V_k - prev_V
        
        # 增量比值
        dS_ratio = dS / prev_dS if prev_dS else 0
        dV_ratio = dV / prev_dV if prev_dV else 0
        
        print(f"{m:<6} {k:<8} {t_k:<18.6f} {S_k:<18.6e} {V_k:<20.6e} {dS:<18.6e} {dV:<20.6e} {dS_ratio:<14.6f} {dV_ratio:<14.6f}")
    else:
        dS = None
        dV = None
        dS_ratio = None
        dV_ratio = None
        print(f"{m:<6} {k:<8} {t_k:<18.6f} {S_k:<18.6e} {V_k:<20.6e} {'-':<18} {'-':<20} {'-':<14} {'-':<14}")
    
    prev_S = S_k
    prev_V = V_k
    prev_dS = dS if dS else S_k
    prev_dV = dV if dV else V_k

# ==================== 与理论预测对比 ====================
print()
print("=" * 100)
print("与理论预测的对比")
print("=" * 100)

print()
print("理论分析：")
print("  零点数增比: Δk_{m+1}/Δk_m = 5")
print("  S(h) ∝ h² → 如果 h 的增长因子为 f，则 ΔS 增长因子为 f²")
print("  V(h) ∝ h³ → 如果 h 的增长因子为 f，则 ΔV 增长因子为 f³")
print()

# 提取有效数据（排除第一行无增量）
valid_m = []
valid_t = []
for m_idx, k in enumerate(zero_return_indices):
    if k > total:
        break
    valid_m.append(m_idx + 1)
    valid_t.append(t_all[k-1])

if len(valid_t) >= 2:
    # h 的增长因子
    h_ratios = [valid_t[i+1]/valid_t[i] for i in range(len(valid_t)-1)]
    print(f"实际 h 增比 (t_{m+1}/t_m):")
    for i, r in enumerate(h_ratios):
        print(f"  m={i+1}→{i+2}: t_ratio = {r:.4f}")
        print(f"    预测 ΔS 增比 = {r**2:.4f}")
        print(f"    预测 ΔV 增比 = {r**3:.4f}")
        print(f"    实际零点数增比 = 5.0")
        print(f"    ΔS 增比 vs 5: {r**2/5:.4f}")
        print(f"    ΔV 增比 vs 5: {r**3/5:.4f}")

# ==================== 层内零点数与 V 增量的关系 ====================
print()
print("=" * 100)
print("关键假设检验：ΔV 是否与层内零点数成正比？")
print("=" * 100)

prev_V_val = None
for m_idx, k in enumerate(zero_return_indices):
    if k > total:
        break
    
    m = m_idx + 1
    t_k = t_all[k-1]
    V_k = V(t_k)
    
    if prev_V_val is not None:
        dV_val = V_k - prev_V_val
        
        # 该层内的零点数
        if m_idx == 0:
            layer_zeros = zero_return_indices[1] - zero_return_indices[0]  # 5
        elif m_idx < len(zero_return_indices) - 1:
            if zero_return_indices[m_idx+1] <= total:
                layer_zeros = zero_return_indices[m_idx+1] - zero_return_indices[m_idx]
            else:
                layer_zeros = total - k
        else:
            layer_zeros = total - k
        
        ratio = dV_val / layer_zeros
        print(f"m={m}: ΔV = {dV_val:.6e}, 层内零点数 = {layer_zeros}, ΔV/零点数 = {ratio:.6e}")
    
    prev_V_val = V_k

# ==================== 新增：S 和 V 的环比分析 ====================
print()
print("=" * 100)
print("新增验证：S 和 V 的环比（相邻零回点处的比值）")
print("=" * 100)

valid_k = []
valid_t_k = []
for k in zero_return_indices:
    if k <= total:
        valid_k.append(k)
        valid_t_k.append(t_all[k-1])

print(f"{'m':<6} {'k_m':<8} {'t_k':<18} {'S(t_k)':<18} {'S环比':<14} {'V(t_k)':<20} {'V环比':<14}")
print("-" * 110)

for i in range(len(valid_k)):
    m = i + 1
    k = valid_k[i]
    t_k = valid_t_k[i]
    S_k = S(t_k)
    V_k = V(t_k)
    
    if i == 0:
        print(f"{m:<6} {k:<8} {t_k:<18.6f} {S_k:<18.6e} {'-':<14} {V_k:<20.6e} {'-':<14}")
    else:
        S_ratio = S_k / S(t_all[valid_k[i-1]-1])
        V_ratio = V_k / V(t_all[valid_k[i-1]-1])
        print(f"{m:<6} {k:<8} {t_k:<18.6f} {S_k:<18.6e} {S_ratio:<14.6f} {V_k:<20.6e} {V_ratio:<14.6f}")

# 理论预测：S ∝ h²，V ∝ h³，零点数增比 = 5
print()
print("理论对比：")
print("  若 S ∝ h²，V ∝ h³，且每层 h 增比 ≈ 2.5-4.0")
print("  则 S 环比 ≈ 6-16，V 环比 ≈ 15-64")
print("  零点数增比 Δk = 5")
print("  观察 S 环比和 V 环比与 5 的幂次关系")

# ==================== 新增：ΔS 和 ΔV 与 5^m 的关系 ====================
print()
print("=" * 100)
print("新增验证：ΔS 和 ΔV 与 5^m 的比例关系")
print("=" * 100)

print(f"{'m':<6} {'Δk=5^m':<12} {'ΔS':<18} {'ΔS/5^m':<16} {'ΔV':<20} {'ΔV/5^m':<16} {'ΔV/ΔS':<14}")
print("-" * 110)

prev_t = None
prev_S_val = None
prev_V_val = None

for m_idx, k in enumerate(zero_return_indices):
    if k > total:
        break
    
    m = m_idx + 1
    t_k = t_all[k-1]
    S_k = S(t_k)
    V_k = V(t_k)
    
    if m_idx == 0:
        prev_t = t_k
        prev_S_val = S_k
        prev_V_val = V_k
        continue
    
    dS = S_k - prev_S_val
    dV = V_k - prev_V_val
    dk = 5 ** (m_idx)  # Δk_m = 5^m，这里m_idx从1开始对应Δk=5^1
    
    dS_per_5m = dS / dk
    dV_per_5m = dV / dk
    dV_dS_ratio = dV / dS if dS != 0 else 0
    
    print(f"{m:<6} {dk:<12} {dS:<18.6e} {dS_per_5m:<16.6e} {dV:<20.6e} {dV_per_5m:<16.6e} {dV_dS_ratio:<14.6f}")
    
    prev_t = t_k
    prev_S_val = S_k
    prev_V_val = V_k

# ==================== 新增：S 的增量与 5 的幂次直接比对 ====================
print()
print("=" * 100)
print("新增验证：ΔS 的增长因子 vs 5 的幂次")
print("=" * 100)

print(f"{'层间':<10} {'ΔS增长因子':<16} {'5^?':<10} {'比值':<12}")
print("-" * 50)

dS_values = []
for m_idx, k in enumerate(zero_return_indices):
    if k > total:
        break
    if m_idx == 0:
        dS_values.append(S(t_all[k-1]))
    else:
        dS_values.append(S(t_all[k-1]) - S(t_all[zero_return_indices[m_idx-1]-1]))

for i in range(2, len(dS_values)):
    growth_factor = dS_values[i] / dS_values[i-1]
    # 找到最接近的 5^x
    power_of_5 = np.log(growth_factor) / np.log(5)
    nearest_5_power = round(power_of_5)
    ratio_to_5 = growth_factor / (5 ** nearest_5_power)
    print(f"m={i}→{i+1}:  {growth_factor:<16.4f} 5^{nearest_5_power:<6} {ratio_to_5:<12.4f}")

print()
print("完成！")