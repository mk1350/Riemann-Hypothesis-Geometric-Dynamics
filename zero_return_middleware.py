import numpy as np
from scipy.special import lambertw

# ==================== 几何公式 ====================
def S(h):
    return (2 * np.pi / np.sqrt(3)) * h**2

def V(h):
    return (4 * np.pi / 9) * h**3

def r_function(t):
    t_safe = np.maximum(t, 2*np.pi + 1e-10)
    return 2 * np.sqrt(3) / np.log(t_safe / (2 * np.pi))

# ==================== N(T) 的逆函数：从零点序号 k 反推高度 T ====================
def N_inverse(k, tol=1e-10, max_iter=100):
    """
    用 N(T) = (T/2π)log(T/2π) - T/2π 的渐进形式
    反解 T，使用牛顿迭代法。
    主项：k ≈ (T/2π)log(T/2π)
    用 Lambert W 函数给出初始猜测
    """
    if k <= 0:
        return 0.0
    
    # 初始猜测：用主项 T ≈ 2πk / log(k)
    # 更精确的初始猜测用 Lambert W
    try:
        # N(T) 的主项：k = (T/2π)log(T/2π)
        # 令 x = log(T/2π)，则 k = (e^x) * x / (2π? 不对)
        # 直接用近似：T ≈ 2πk / log(k)
        T = 2 * np.pi * k / np.log(k + 1)
    except:
        T = 2 * np.pi * k / np.log(k + 1)
    
    # 牛顿迭代
    for _ in range(max_iter):
        # N(T) ≈ (T/2π)log(T/2π) - T/2π + O(log T)
        log_term = np.log(T / (2 * np.pi))
        N_val = (T / (2 * np.pi)) * log_term - T / (2 * np.pi)
        # 导数：dN/dT ≈ (1/2π)log(T/2π)
        dN_dT = log_term / (2 * np.pi)
        
        diff = N_val - k
        if abs(diff) < tol:
            break
        T = T - diff / dN_dT
        
        if T <= 2 * np.pi:
            T = 2 * np.pi + 1e-10
    
    return T

# ==================== 数据 ====================
DATA_FILE = r"F:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_100000.npy"
t_all = np.load(DATA_FILE)
total = len(t_all)

zero_return_indices = [2, 7, 32, 157, 782, 3907, 19532, 97657]

print("=" * 100)
print("核心验证：用 N(T) 的逆函数连接 k_m 和 t_k")
print("=" * 100)
print()

# ==================== 对比：理论 t_k vs 实际 t_k ====================
print(f"{'m':<6} {'k_m':<8} {'理论t_k':<18} {'实际t_k':<18} {'偏差%':<14}")
print("-" * 70)

for m_idx, k in enumerate(zero_return_indices):
    m = m_idx + 1
    
    # 理论值：N^{-1}(k)
    t_theory = N_inverse(k)
    
    # 实际值
    if k <= total:
        t_actual = t_all[k-1]
        deviation = abs(t_theory - t_actual) / t_actual * 100
        print(f"{m:<6} {k:<8} {t_theory:<18.6f} {t_actual:<18.6f} {deviation:<14.6f}")
    else:
        print(f"{m:<6} {k:<8} {t_theory:<18.6f} (超出数据范围)")

# ==================== 用理论 t_k 计算几何量并对比 ====================
print()
print("=" * 100)
print("用理论 t_k 计算 S 和 V，与直接用实际 t_k 计算的结果对比")
print("=" * 100)
print(f"{'m':<6} {'理论S':<18} {'实际S':<18} {'偏差%':<14} {'理论V':<20} {'实际V':<20} {'偏差%':<14}")
print("-" * 110)

for m_idx, k in enumerate(zero_return_indices):
    m = m_idx + 1
    t_theory = N_inverse(k)
    S_theory = S(t_theory)
    V_theory = V(t_theory)
    
    if k <= total:
        t_actual = t_all[k-1]
        S_actual = S(t_actual)
        V_actual = V(t_actual)
        S_dev = abs(S_theory - S_actual) / S_actual * 100
        V_dev = abs(V_theory - V_actual) / V_actual * 100
        print(f"{m:<6} {S_theory:<18.6e} {S_actual:<18.6e} {S_dev:<14.6f} {V_theory:<20.6e} {V_actual:<20.6e} {V_dev:<14.6f}")
    else:
        print(f"{m:<6} {S_theory:<18.6e} (超出)         {V_theory:<20.6e} (超出)")

# ==================== 核心：用理论 t_k 重算验证1-4 ====================
print()
print("=" * 100)
print("用理论 t_k 重算验证闭环（无需实际零点数据）")
print("=" * 100)

valid_k = [k for k in zero_return_indices]
t_theory_list = [N_inverse(k) for k in valid_k]

# 验证1：ΔV/ΔS
print()
print("【理论验证1】ΔV/ΔS 与 h 的关系")
print("-" * 70)
for i in range(len(t_theory_list)-1):
    h1, h2 = t_theory_list[i], t_theory_list[i+1]
    dV_val = V(h2) - V(h1)
    dS_val = S(h2) - S(h1)
    ratio = dV_val / dS_val
    h_mid = (h1 + h2) / 2
    normalized = ratio / h_mid
    print(f"m={i+1}→{i+2}: ΔV/ΔS={ratio:.4f}, h_mid={h_mid:.2f}, (ΔV/ΔS)/h_mid={normalized:.6f}")

# 验证4：S环比的对数增长率
print()
print("【理论验证4】S 环比的对数增长率")
print("-" * 55)
S_theory_list = [S(h) for h in t_theory_list]
for i in range(1, len(S_theory_list)):
    ratio_S = S_theory_list[i] / S_theory_list[i-1]
    log5_ratio = np.log(ratio_S) / np.log(5)
    print(f"m={i}→{i+1}: S环比={ratio_S:.6f}, log5(S环比)={log5_ratio:.6f}")

# 理论极限
print(f"\n理论极限: 5^(2/3) = {5**(2/3):.6f}, log5(5^(2/3)) = {2/3:.6f}")

print()
print("完成！")