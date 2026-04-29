import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 圆锥参数设置 ====================
H_max = 50.0
R_ratio = 2/np.sqrt(3)  # r(h) = 2h/√3

# 选取代表性零点高度
zero_heights = np.array([14.13, 21.02, 25.01, 30.42, 32.93, 37.58, 40.91, 43.32, 48.00, 49.77])
zero_heights_scaled = zero_heights * 0.8

# 特征高度
feature_height1 = 25.0
feature_height2 = 40.0

# ==================== 创建图形 ====================
fig = plt.figure(figsize=(18, 14))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=25, azim=-45)

# ==================== 1. 圆锥包络面（顶点在 (0.5, 0, 0)）====================
theta_cone = np.linspace(0, 2*np.pi, 60)
z_cone = np.linspace(0, H_max, 50)
Theta_cone, Z_cone = np.meshgrid(theta_cone, z_cone)
R_cone = R_ratio * Z_cone
X_cone = 0.5 + R_cone * np.cos(Theta_cone)  # 圆心在 x=0.5
Y_cone = R_cone * np.sin(Theta_cone)

ax.plot_surface(X_cone, Y_cone, Z_cone, alpha=0.12, color='lightblue', edgecolor=None)

# ==================== 2. 临界线（圆锥主轴，x=0.5）====================
z_axis = np.linspace(0, H_max, 100)
critical_x = 0.5
ax.plot(np.full_like(z_axis, critical_x), np.zeros_like(z_axis), z_axis, 
        'r-', linewidth=2.0, alpha=0.8, label=f'临界线 (主轴, x=0.5)')

# ==================== 3. 零点位置（在临界线上）====================
# 零点绝对三维坐标：(0.5, t_n, t_n)
for i, h in enumerate(zero_heights_scaled):
    ax.scatter(critical_x, h, h, color='gold', s=80, edgecolors='darkorange', 
               linewidths=1.5, zorder=5)

# ==================== 4. 共振圆及其60°交点 ====================
def draw_resonance_circle(ax, height, color='blue', alpha=0.6, linewidth=2):
    """绘制共振圆及其60°视线交点"""
    r = R_ratio * height
    center_x = critical_x
    center_y = 0
    
    # 圆周
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = center_x + r * np.cos(theta)
    y_circle = center_y + r * np.sin(theta)
    z_circle = np.full_like(theta, height)
    ax.plot(x_circle, y_circle, z_circle, color=color, linewidth=linewidth, alpha=alpha)
    
    # 半透明截面圆盘
    theta_fill = np.linspace(0, 2*np.pi, 30)
    r_fill = np.linspace(0, r, 15)
    Theta_fill, R_fill = np.meshgrid(theta_fill, r_fill)
    X_fill = center_x + R_fill * np.cos(Theta_fill)
    Y_fill = center_y + R_fill * np.sin(Theta_fill)
    Z_fill = np.full_like(X_fill, height)
    ax.plot_surface(X_fill, Y_fill, Z_fill, alpha=0.15, color=color, edgecolor=None)
    
    return r

r1 = draw_resonance_circle(ax, feature_height1, color='royalblue', alpha=0.7)
r2 = draw_resonance_circle(ax, feature_height2, color='crimson', alpha=0.7)

# ==================== 5. 60°视线交点（从原点到共振圆）====================
# 从复平面原点(0,0,0)出发，仰角60°，与共振圆交于：
# (0.5 + t_n/√3, t_n, t_n)
for i, h in enumerate(zero_heights_scaled):
    r = R_ratio * h
    angle = np.pi/3  # 60°
    x0 = critical_x + r * np.cos(angle)
    y0 = r * np.sin(angle)
    z0 = h
    
    # 60°视线交点（与零点在同一高度，但在共振圆上）
    ax.scatter(x0, y0, z0, color='lime', s=40, edgecolors='darkgreen', 
               linewidths=1.0, zorder=5, alpha=0.8)
    
    # 从原点(0,0,0)到60°交点的视线
    ax.plot([0, x0], [0, y0], [0, h], 'orange', linewidth=0.5, alpha=0.3)
    
    # 从60°交点到临界线上零点的水平连线（虚线）
    ax.plot([x0, critical_x], [y0, h], [h, h], 'gray', linewidth=0.5, alpha=0.4, linestyle=':')

# ==================== 6. 60°角度标注 ====================
lowest_h = zero_heights_scaled[0]
lowest_r = R_ratio * lowest_h
lowest_x = critical_x + lowest_r * np.cos(np.pi/3)
lowest_y = lowest_r * np.sin(np.pi/3)

ax.plot([0, lowest_x], [0, 0], [0, 0], color='gray', linestyle='-', linewidth=1, alpha=0.5)
ax.plot([0, lowest_x], [0, lowest_y], [0, 0], color='gray', linestyle='-', linewidth=1, alpha=0.5)
ax.plot([0, lowest_x], [0, lowest_y], [0, lowest_h], color='orange', linestyle='-', linewidth=1, alpha=0.4)

mid_h = lowest_h / 3
ax.text(lowest_x/2 + 0.8, lowest_y/2 + 0.8, mid_h, '60°', color='darkorange', fontsize=11, fontweight='bold')

# ==================== 7. 几何量标注 ====================
ax.text(critical_x + r2*0.5, r2*0.5, feature_height2 + 2, 
        'C(h)∝h', color='crimson', fontsize=10, fontweight='bold')
ax.text(critical_x - r2*1.2, r2*0.6, feature_height2 + 1, 
        'dC/dh∝const', color='purple', fontsize=10, fontweight='bold')

# ==================== 8. 变化率箭头 ====================
mid_height = (feature_height1 + feature_height2) / 2
mid_r = R_ratio * mid_height

ax.quiver(critical_x - mid_r*0.7, mid_r*0.3, mid_height - 3,
          0, 0, 7,
          color='purple', linewidth=2, arrow_length_ratio=0.3)
ax.text(critical_x - mid_r*0.7 - 1.5, mid_r*0.3, mid_height + 3,
        "dC/dh ∝ const → Φ'(t) = -c₂", color='purple', fontsize=10, fontweight='bold')

# ==================== 9. 包络线 ====================
for angle_sample in [0, np.pi/2, np.pi, 3*np.pi/2]:
    z_sample = np.linspace(0, H_max, 100)
    r_sample = R_ratio * z_sample
    x_sample = critical_x + r_sample * np.cos(angle_sample)
    y_sample = r_sample * np.sin(angle_sample)
    ax.plot(x_sample, y_sample, z_sample, color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

# ==================== 10. 坐标轴和标题 ====================
ax.set_xlabel('X (Re(s))', fontsize=11)
ax.set_ylabel('Y (Im(s))', fontsize=11)
ax.set_zlabel('Z (高度 = Im(s) = t)', fontsize=11)

ax.set_title('黎曼零点几何圆锥构造\n'
             "Φ'(t) = -c₂ (常数), 由 dC/dh = 4π/√3 (常数) 导出",
             fontsize=13, fontweight='bold', pad=25)

# 坐标轴范围
max_r = R_ratio * H_max
ax.set_xlim(-max_r, max_r + 1)
ax.set_ylim(-max_r, max_r)
ax.set_zlim(0, H_max)

# X轴刻度标注0.5（临界线位置）
ax.set_xticks([0, 0.5, 50])
ax.set_xticklabels(['0', '0.5\n(临界线)', '50'])

ax.legend(loc='upper left', fontsize=9)

# ==================== 11. 图例和底部说明 ====================
fig.text(0.5, 0.02,
         '圆锥构造：临界线（红色，x=0.5）为绝对共用主轴，圆锥顶点(0.5,0,0)。\n'
         '金色圆点：零点，绝对三维坐标 (0.5, tₙ, tₙ)，位于临界线上。\n'
         '绿色圆点：共振圆上60°视线交点，坐标 (0.5 + tₙ/√3, tₙ, tₙ)。\n'
         '橙色虚线：从复平面原点(0,0,0)到60°视线交点。灰色虚线：60°视线交点到零点的水平连线。\n'
         '截面周长变化率 dC/dh = 4π/√3 为常数 → 垂直势梯度 Φ\'(t) = -c₂ 为常数。',
         fontsize=9, ha='center', va='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()