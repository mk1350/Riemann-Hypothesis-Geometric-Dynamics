"""
================================================================================
拟合动力学方程 (Fitted Dynamical Equation)
================================================================================
功能: 用训练集优化拟合参数 m 和 γ，然后做滚动样本外预测，验证方程自洽性。
      支持正向零点(正半平面)和负向零点(负半平面)，通过对称性自动处理力的方向。

方程: t_n = 2*t_{n-1} - t_{n-2} - (1/m)(Φ'(t_{n-1}) + γ*(t_{n-1} - t_{n-2}))
      系数2 = 1/cos60° (几何锁定)

负向零点对称性:
      正向: t递增, 力 = -c₂ + γ*v, Φ' = -c₂
      负向: t递减(-14到-5447), 力 = c₂ - γ*v, Φ' = +c₂
      即力的表达式整体反号，保证预测值对称

数据: LMFDB 黎曼zeta函数非平凡零点虚部
================================================================================
"""

import numpy as np
from scipy.optimize import minimize

# ==================== 配置 ====================
# 数据文件路径 (Data file path)
DATA_FILE = r"D:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_5000.npy"
# DATA_FILE = r"D:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_50000.npy"

# 训练集大小列表 (Training set sizes)
TRAIN_SIZES = [
    10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
    120, 140, 160, 180, 200,
    250, 300, 350, 400, 450, 500,
    600, 700, 800, 900, 1000,
    1200, 1400, 1600, 1800, 2000,
    2500, 3000, 3500, 4000
]

# ==================== 核心函数 (Core Functions) ====================

def fit_params(t_data):
    """拟合 m 和 γ (Fit m and gamma)
    
    动力学方程:
    t_n = 2*t_{n-1} - t_{n-2} - (1/m)(Φ'(t_{n-1}) + γ*(t_{n-1} - t_{n-2}))
    
    牛顿形式 (Newtonian form):
    (t_n - 2*t_{n-1} + t_{n-2}) = -(1/m)*Φ'(t_{n-1}) - (γ/m)*(t_{n-1} - t_{n-2})
    离散加速度 = -(1/m)*势场梯度 - (γ/m)*离散速度
    acceleration = -(1/m)*potential_gradient - (gamma/m)*velocity
    
    参数:
        t_data: 零点序列 (zero sequence)
    返回:
        m, gamma: 拟合参数
        acceleration: 离散加速度序列
        velocity: 离散速度序列
    """
    n = len(t_data)
    # 离散加速度 (discrete acceleration): a_i = t_i - 2*t_{i-1} + t_{i-2}
    acceleration = np.array([t_data[i] - 2*t_data[i-1] + t_data[i-2] for i in range(2, n)])
    # 离散速度 (discrete velocity): v_i = t_{i-1} - t_{i-2}
    velocity = np.array([t_data[i-1] - t_data[i-2] for i in range(2, n)])
    
    def objective(params):
        m, gamma = params
        # Φ'(t_{n-1}) = -m * acceleration - gamma * velocity
        phi_prime = -m * acceleration - gamma * velocity
        # 最小化 Φ'(t) 的平滑度 (minimize smoothness of Φ'(t))
        return np.sum(np.diff(phi_prime)**2) + 0.01*(m**2 + gamma**2)
    
    # 边界条件 (bounds)
    res = minimize(objective, [0.5, 0.2], 
                   bounds=[(0.001, 2), (0.0001, 1)], 
                   method='L-BFGS-B')
    return res.x[0], res.x[1], acceleration, velocity


def predict_window(t_all, train_size, m, gamma, direction='positive'):
    """滚动预测 (Rolling prediction)
    
    用固定窗宽做样本外滚动预测。支持正向和负向零点。
    Out-of-sample rolling prediction with fixed window size.
    Supports both positive and negative zeros.
    
    参数:
        t_all: 完整零点序列 (full zero sequence)
        train_size: 训练窗口大小 (training window size)
        m, gamma: 固定参数 (fixed parameters)
        direction: 'positive' 正向零点(递增) / 'negative' 负向零点(递减)
    返回:
        preds: 预测值数组
        acts: 实际值数组
    """
    preds, acts = [], []
    
    for i in range(train_size, len(t_all)):
        # 当前窗口 (current window)
        w = t_all[i - train_size : i]
        nw = len(w)
        
        # 窗口内的加速度和速度 (acceleration and velocity in window)
        acceleration_win = np.array([w[j] - 2*w[j-1] + w[j-2] for j in range(2, nw)])
        velocity_win = np.array([w[j-1] - w[j-2] for j in range(2, nw)])
        
        # 计算 Φ'(t) (compute Φ'(t))
        phi_prime_win = -m * acceleration_win - gamma * velocity_win
        
        # 预测下一个零点 (predict next zero)
        # t_n = 2*t_{n-1} - t_{n-2} - (1/m)*(Φ'(t_{n-1}) + γ*(t_{n-1} - t_{n-2}))
        pred = (2 * t_all[i-1] 
                - t_all[i-2] 
                - (1/m) * (phi_prime_win[-1] + gamma * (t_all[i-1] - t_all[i-2])))
        
        preds.append(pred)
        acts.append(t_all[i])
    
    return np.array(preds), np.array(acts)


def evaluate(preds, acts, label):
    """评估预测精度 (Evaluate prediction accuracy)
    
    参数:
        preds: 预测值 (predictions)
        acts: 实际值 (actuals)
        label: 标签 (label for printing)
    返回:
        rmse, mae, rel_err
    """
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(np.abs(acts)) * 100
    avg_spacing = np.mean(np.abs(np.diff(acts)))
    rmse_ratio = rmse / avg_spacing * 100
    
    print(f"\n{label}:")
    print(f"  预测数量 (Predictions): {len(preds)}")
    print(f"  RMSE = {rmse:.8f}")
    print(f"  MAE = {mae:.8f}")
    print(f"  相对误差 (Relative error) = {rel_err:.8f}%")
    print(f"  平均零点间距 (Avg spacing) = {avg_spacing:.4f}")
    print(f"  RMSE / 平均间距 = {rmse_ratio:.4f}%")
    
    return rmse, mae, rel_err


# ==================== 主流程 (Main) ====================

print("=" * 90)
print("拟合动力学方程验证 - Fitted Dynamical Equation Verification")
print("=" * 90)

# 加载正向零点 (Load positive zeros)
t_positive = np.load(DATA_FILE)
total = len(t_positive)
print(f"加载零点数据 (Loaded zeros): {total}")
print(f"正向零点范围 (Positive zero range): {t_positive[0]:.6f} ~ {t_positive[-1]:.6f}")

# 构造负向零点 (Construct negative zeros)
t_negative = -t_positive  # 关于实轴对称，保持原序 [-14, -21, -25, ...]
print(f"负向零点范围 (Negative zero range): {t_negative[0]:.6f} ~ {t_negative[-1]:.6f}")
print()
print("-" * 90)

# ==================== 正向零点 (Positive Zeros) ====================
print("\n" + "=" * 90)
print("正向零点验证 - Positive Zeros Verification (递增序列, ascending sequence)")
print("=" * 90)
print(f"{'训练集':<8} {'验证集':<8} {'m':<14} {'γ':<14} {'Φ均值':<16} {'RMSE':<14} {'MAE':<14} {'相对误差':<12}")
print(f"{'Train':<8} {'Test':<8} {'m':<14} {'γ':<14} {'Φ mean':<16} {'RMSE':<14} {'MAE':<14} {'Rel err':<12}")
print("-" * 90)

results_pos = []

for train_size in TRAIN_SIZES:
    if train_size >= total - 1:
        continue
    
    t_train = t_positive[:train_size]
    
    # 拟合参数 (Fit parameters)
    m, gamma, acceleration, velocity = fit_params(t_train)
    phi_prime_train = -m * acceleration - gamma * velocity
    
    # 滚动预测 (Rolling prediction)
    preds, acts = predict_window(t_positive, train_size, m, gamma, direction='positive')
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(acts) * 100
    
    results_pos.append({
        'train_size': train_size,
        'test_size': len(preds),
        'm': m, 'gamma': gamma,
        'phi_mean': np.mean(phi_prime_train),
        'rmse': rmse, 'mae': mae,
        'rel_err': rel_err
    })
    
    print(f"{train_size:<8} {len(preds):<8} {m:<14.8f} {gamma:<14.8f} "
          f"{np.mean(phi_prime_train):<16.8f} {rmse:<14.8f} {mae:<14.8f} {rel_err:<12.8f}")

# ==================== 负向零点 (Negative Zeros) ====================
print("\n" + "=" * 90)
print("负向零点验证 - Negative Zeros Verification (递减序列, descending sequence)")
print("=" * 90)
print(f"{'训练集':<8} {'验证集':<8} {'m':<14} {'γ':<14} {'Φ均值':<16} {'RMSE':<14} {'MAE':<14} {'相对误差':<12}")
print(f"{'Train':<8} {'Test':<8} {'m':<14} {'γ':<14} {'Φ mean':<16} {'RMSE':<14} {'MAE':<14} {'Rel err':<12}")
print("-" * 90)

results_neg = []

for train_size in TRAIN_SIZES:
    if train_size >= total - 1:
        continue
    
    t_train = t_negative[:train_size]
    
    # 拟合参数 (Fit parameters)
    m, gamma_neg, acceleration, velocity = fit_params(t_train)
    # 注意：负向零点的Φ'会自动取正号，γ也自动适配
    phi_prime_train = -m * acceleration - gamma_neg * velocity
    
    # 滚动预测 (Rolling prediction)
    preds, acts = predict_window(t_negative, train_size, m, gamma_neg, direction='negative')
    errors = acts - preds
    rmse = np.sqrt(np.mean(errors**2))
    mae = np.mean(np.abs(errors))
    rel_err = mae / np.mean(np.abs(acts)) * 100
    
    results_neg.append({
        'train_size': train_size,
        'test_size': len(preds),
        'm': m, 'gamma': gamma_neg,
        'phi_mean': np.mean(phi_prime_train),
        'rmse': rmse, 'mae': mae,
        'rel_err': rel_err
    })
    
    print(f"{train_size:<8} {len(preds):<8} {m:<14.8f} {gamma_neg:<14.8f} "
          f"{np.mean(phi_prime_train):<16.8f} {rmse:<14.8f} {mae:<14.8f} {rel_err:<12.8f}")

# ==================== 正负对称性检验 (Symmetry Check) ====================
print("\n" + "=" * 90)
print("正负零点对称性检验 - Positive vs Negative Symmetry Check")
print("=" * 90)

# 比较最后一组（最大训练集）的结果
rmse_pos_final = results_pos[-1]['rmse']
rmse_neg_final = results_neg[-1]['rmse']
m_pos_final = results_pos[-1]['m']
m_neg_final = results_neg[-1]['m']
phi_pos_final = results_pos[-1]['phi_mean']
phi_neg_final = results_neg[-1]['phi_mean']

print(f"正向 RMSE = {rmse_pos_final:.8f}, 负向 RMSE = {rmse_neg_final:.8f}")
print(f"RMSE 比值 (正/负) = {rmse_pos_final/rmse_neg_final:.8f}")
print(f"正向 m = {m_pos_final:.8f}, 负向 m = {m_neg_final:.8f}")
print(f"正向 Φ'均值 = {phi_pos_final:.8f}, 负向 Φ'均值 = {phi_neg_final:.8f}")

if abs(rmse_pos_final - rmse_neg_final) < 1e-6:
    print("★ 正向与负向 RMSE 完全一致，对称性验证通过。")
elif abs(rmse_pos_final - rmse_neg_final) < 0.01:
    print(f"★ 正向与负向 RMSE 高度一致（差异 < 0.01），对称性良好。")
else:
    print(f"差异较大，需要检查。")

print("\n完成 (Done)!")