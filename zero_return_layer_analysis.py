import numpy as np

# ==================== 配置 ====================
DATA_FILE = r"F:\60_Degree_Invariant_Riemann_Hypothesis\riemann_zeros_data\riemann_zeros_50000.npy"

# ==================== 加载数据 ====================
t_all = np.load(DATA_FILE)
total = len(t_all)

# 一阶、二阶、三阶差分
delta_1 = np.diff(t_all)
delta_2 = np.diff(delta_1)
delta_3 = np.diff(delta_2)

# 层边界（零回点 k_m = (5^m+3)/4）
# k = 2, 7, 32, 157, 782, 3907, 19532...
layer_boundaries = [2, 7, 32, 157, 782, 3907, total]  # 最后一个用数据上限

print("=" * 100)
print("零回点作为层边界 — 密度分层分析")
print("=" * 100)
print(f"零点总数: {total}")
print(f"层边界（零回点）: {layer_boundaries[:-1]}")
print(f"共 {len(layer_boundaries)-1} 层")
print()

# ==================== 逐层统计 ====================
print("=" * 140)
print(f"{'层':<6} {'零点区间':<16} {'零点数':<10} {'t范围':<22} {'一阶均值':<12} {'一阶std':<10} {'二阶abs均值':<14} {'二阶std':<12} {'三阶abs均值':<14} {'理论间距均值':<14}")
print("-" * 140)

layer_results = []

for i in range(len(layer_boundaries) - 1):
    k_start = layer_boundaries[i]
    k_end = layer_boundaries[i+1] - 1  # 该层最后一个零点的索引（0-based）
    
    if k_start >= total:
        continue
    if k_end >= total:
        k_end = total - 1
    
    # 该层内的零点（包含起点，不包含下一层的起点）
    t_layer = t_all[k_start-1 : k_end+1]  # k是1-based序号，转为0-based索引
    
    if len(t_layer) < 3:
        continue
    
    # 层内差分
    d1_layer = np.diff(t_layer)
    d2_layer = np.diff(d1_layer)
    d3_layer = np.diff(d2_layer)
    
    # 该层对应的理论间距
    t_mid_layer = (t_layer[:-1] + t_layer[1:]) / 2
    theory_layer = 2 * np.pi / np.log(t_mid_layer / (2 * np.pi))
    
    layer_results.append({
        'layer': i+1,
        'k_start': k_start,
        'k_end': k_end,
        'count': len(t_layer)-1,
        't_range': f"[{t_layer[0]:.2f}, {t_layer[-1]:.2f}]",
        'd1_mean': np.mean(d1_layer),
        'd1_std': np.std(d1_layer),
        'd2_abs_mean': np.mean(np.abs(d2_layer)),
        'd2_std': np.std(d2_layer),
        'd3_abs_mean': np.mean(np.abs(d3_layer)),
        'theory_mean': np.mean(theory_layer),
        'd1_layer': d1_layer,
        't_mid': t_mid_layer
    })
    
    print(f"{i+1:<6} t_{k_start}-t_{k_end:<10} {len(t_layer)-1:<10} {f'[{t_layer[0]:.2f}, {t_layer[-1]:.2f}]':<22} {np.mean(d1_layer):<12.4f} {np.std(d1_layer):<10.4f} {np.mean(np.abs(d2_layer)):<14.6f} {np.std(d2_layer):<12.6f} {np.mean(np.abs(d3_layer)):<14.8f} {np.mean(theory_layer):<14.4f}")

# ==================== 跨层对比 ====================
print()
print("=" * 100)
print("跨层对比 — 层间差异显著性")
print("=" * 100)
print(f"{'相邻层':<12} {'一阶均值差':<14} {'二阶均值差':<14} {'零点数增比':<14} {'层间距(t)':<16} {'密度翻倍?':<14}")
print("-" * 80)

for i in range(len(layer_results)-1):
    d1_diff = abs(layer_results[i]['d1_mean'] - layer_results[i+1]['d1_mean'])
    d2_diff = abs(layer_results[i]['d2_abs_mean'] - layer_results[i+1]['d2_abs_mean'])
    count_ratio = layer_results[i+1]['count'] / layer_results[i]['count']
    
    t_gap = layer_results[i+1]['t_range'].split('[')[1].split(',')[0]
    t_gap = float(t_gap)
    t_start = layer_results[i]['t_range'].split('[')[1].split(',')[0]
    t_start = float(t_start)
    t_span = t_gap / t_start
    
    density_double = "是 ✓" if 1.8 < count_ratio < 10 else f"~{count_ratio:.1f}倍"
    
    print(f"层{i+1}→层{i+2:<7} {d1_diff:<14.4f} {d2_diff:<14.6f} {count_ratio:<14.4f} {t_span:<16.4f} {density_double:<14}")

# ==================== 层内一致性 ====================
print()
print("=" * 100)
print("层内一致性 — 每层一阶差分的波动（变异系数）")
print("=" * 100)
print(f"{'层':<6} {'零点数':<10} {'一阶均值':<12} {'一阶std':<10} {'变异系数%':<12} {'是否稳定':<14}")
print("-" * 70)

for res in layer_results:
    cv = res['d1_std'] / res['d1_mean'] * 100  # 变异系数
    stable = "稳定 ✓" if cv < 30 else f"波动 ({cv:.1f}%)"
    print(f"{res['layer']:<6} {res['count']:<10} {res['d1_mean']:<12.4f} {res['d1_std']:<10.4f} {cv:<12.2f} {stable:<14}")

# ==================== 与密度函数的对照 ====================
print()
print("=" * 100)
print("层内实际间距 vs 密度函数理论间距")
print("=" * 100)
print(f"{'层':<6} {'实际间距均值':<14} {'理论间距均值':<14} {'比值':<12} {'比值std':<12}")
print("-" * 65)

for res in layer_results:
    ratio_layer = res['d1_layer'] / (2 * np.pi / np.log(res['t_mid'] / (2 * np.pi)))
    ratio_mean = np.mean(ratio_layer)
    ratio_std = np.std(ratio_layer)
    print(f"{res['layer']:<6} {res['d1_mean']:<14.4f} {res['theory_mean']:<14.4f} {ratio_mean:<12.4f} {ratio_std:<12.4f}")

# ==================== 层间一阶差分的跃迁幅度 ====================
print()
print("=" * 100)
print("关键发现：层间一阶差分跃迁 vs 层内波动")
print("=" * 100)

for i in range(len(layer_results)-1):
    within_layer_std = layer_results[i]['d1_std']
    between_layer_diff = abs(layer_results[i]['d1_mean'] - layer_results[i+1]['d1_mean'])
    
    # 层间差异是层内波动的多少倍
    significance = between_layer_diff / within_layer_std if within_layer_std > 0 else float('inf')
    
    print(f"层{i+1}→层{i+2}: 层间差={between_layer_diff:.4f}, 层内std={within_layer_std:.4f}, "
          f"显著性={significance:.1f}倍 {'★ 显著' if significance > 2 else ''}")

print()
print("完成！")