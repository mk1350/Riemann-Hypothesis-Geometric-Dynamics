import numpy as np

# ==================== 设置 ====================
DATA_FILE = r"D:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_50000.npy"

COEFF_2 = 2.0
c2 = 0.001 * np.pi / np.sqrt(3)  # mπ/√3, m=0.001
m_fixed = 0.001

# ==================== 加载数据 ====================
t_all = np.load(DATA_FILE)
total = len(t_all)

print(f"加载 {total} 个零点")
print(f"t 范围: {t_all[0]:.2f} ~ {t_all[-1]:.2f}")
print()

# ==================== 三种模型的预测 ====================

def predict_with_r_function(t_seq, r_func):
    """用比值函数 r(t) 预测，r = m/γ，γ = m/r"""
    n = len(t_seq)
    preds = []
    acts = []
    for i in range(2, n):
        t_prev = t_seq[i-1]
        r_val = r_func(t_prev)
        gamma_val = m_fixed / r_val
        
        phi_prime = -c2
        pred = (COEFF_2 * t_seq[i-1] 
                - t_seq[i-2] 
                - (1/m_fixed) * (phi_prime + gamma_val * (t_seq[i-1] - t_seq[i-2])))
        preds.append(pred)
        acts.append(t_seq[i])
    return np.array(preds), np.array(acts)


def predict_with_fixed_r(t_seq, r_fixed):
    """用固定比值 r 预测"""
    n = len(t_seq)
    preds = []
    acts = []
    gamma_fixed = m_fixed / r_fixed
    for i in range(2, n):
        phi_prime = -c2
        pred = (COEFF_2 * t_seq[i-1] 
                - t_seq[i-2] 
                - (1/m_fixed) * (phi_prime + gamma_fixed * (t_seq[i-1] - t_seq[i-2])))
        preds.append(pred)
        acts.append(t_seq[i])
    return np.array(preds), np.array(acts)


def evaluate(preds, acts, label):
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(np.abs(acts)) * 100
    print(f"\n{label}:")
    print(f"  RMSE = {rmse:.8f}")
    print(f"  MAE = {mae:.8f}")
    print(f"  相对误差 = {rel_err:.8f}%")
    return rmse


# ==================== 定义比值函数 ====================
def r_log(t):
    """对数衰减比值函数 r = 2√3 / log(t/2π)"""
    # 保护：t 必须 > 2π
    t_safe = np.maximum(t, 2*np.pi + 1e-10)
    return 2 * np.sqrt(3) / np.log(t_safe / (2 * np.pi))

# def r_constant_0625(t):
#     return 0.625

# def r_constant_0505(t):
#     return 0.505


# ==================== 打印前几个点的 r 值 ====================
print("=" * 60)
print("前20个预测点的 r 值对比")
print("=" * 60)
print(f"{'n':<6} {'t_{n-1}':<18} {'r_log':<14} {'r_0625':<14} {'r_0505':<14}")
print("-" * 60)
for i in range(2, min(22, total)):
    t_prev = t_all[i-1]
    print(f"{i:<6} {t_prev:<18.6f} {r_log(t_prev):<14.6f} {0.625:<14} {0.505:<14}")

# ==================== 全序列验证 ====================
print()
print("=" * 60)
print("全序列验证（预测 3 ~ 50000）")
print("=" * 60)

preds_log, acts_log = predict_with_r_function(t_all, r_log)
rmse_log = evaluate(preds_log, acts_log, "对数衰减 r(t) = 2√3 / log(t/2π)")

preds_0625, acts_0625 = predict_with_fixed_r(t_all, 0.625)
rmse_0625 = evaluate(preds_0625, acts_0625, "固定 r = 0.625 (最优妥协)")

preds_0505, acts_0505 = predict_with_fixed_r(t_all, 0.505)
rmse_0505 = evaluate(preds_0505, acts_0505, "固定 r = 0.505 (结构平衡)")

# ==================== 逐段对比 ====================
print()
print("=" * 80)
print("逐500个零点 RMSE 对比")
print("=" * 80)
print(f"{'零点范围':<16} {'r_log RMSE':<16} {'r_0625 RMSE':<16} {'r_0505 RMSE':<16}")
print("-" * 65)

for start in range(2, total, 500):
    end = min(start + 500, total)
    
    seg_preds_log = []
    seg_preds_0625 = []
    seg_preds_0505 = []
    seg_acts = []
    
    for i in range(start, end):
        t_prev = t_all[i-1]
        
        # 对数衰减
        r_val = r_log(t_prev)
        gamma_val = m_fixed / r_val
        pred_log = (COEFF_2 * t_all[i-1] - t_all[i-2] 
                    - (1/m_fixed) * (-c2 + gamma_val * (t_all[i-1] - t_all[i-2])))
        seg_preds_log.append(pred_log)
        
        # 固定 0.625
        gamma_0625 = m_fixed / 0.625
        pred_0625 = (COEFF_2 * t_all[i-1] - t_all[i-2] 
                     - (1/m_fixed) * (-c2 + gamma_0625 * (t_all[i-1] - t_all[i-2])))
        seg_preds_0625.append(pred_0625)
        
        # 固定 0.505
        gamma_0505 = m_fixed / 0.505
        pred_0505 = (COEFF_2 * t_all[i-1] - t_all[i-2] 
                     - (1/m_fixed) * (-c2 + gamma_0505 * (t_all[i-1] - t_all[i-2])))
        seg_preds_0505.append(pred_0505)
        
        seg_acts.append(t_all[i])
    
    seg_preds_log = np.array(seg_preds_log)
    seg_preds_0625 = np.array(seg_preds_0625)
    seg_preds_0505 = np.array(seg_preds_0505)
    seg_acts = np.array(seg_acts)
    
    rmse_log_seg = np.sqrt(np.mean((seg_acts - seg_preds_log)**2))
    rmse_0625_seg = np.sqrt(np.mean((seg_acts - seg_preds_0625)**2))
    rmse_0505_seg = np.sqrt(np.mean((seg_acts - seg_preds_0505)**2))
    
    print(f"t_{start}-t_{end:<5} {rmse_log_seg:<16.8f} {rmse_0625_seg:<16.8f} {rmse_0505_seg:<16.8f}")

print()
print("完成！")