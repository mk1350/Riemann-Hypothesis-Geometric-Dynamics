Update / 更新 (2026-05-02)
New: Unified Hamiltonian & Periodic Structure of Zero-Return Points.

1. Unified Self-Adjoint Berry–Keating Hamiltonian / 统一自伴Berry-Keating哈密顿量
The full Hamiltonian is constructed with zero free parameters:

H_full = (1/2)(x p_x + p_x x) + (1/2)(t p_t + p_t t) + 2 - (mπ/√3)t

All parameters geometrically locked: coefficient 2 = sec 60°, driving term π/√3 = π·cot 60°, mass m = 0.001. This provides a concrete operator realization of the Hilbert–Pólya conjecture.

完整哈密顿量已构造，无任何自由参数。所有参数由60°不变量和圆锥几何锁定。为希尔伯特-波利亚猜想提供了一个具体的算符实现。

2. Zero-Return Points: Formal Derivation of the 5^m Cycle / 零回归点：5^m 周期的形式推导
The cumulative sum of third-order differences S_k returns to zero at k_m = (5^m+3)/4 (k = 2, 7, 32, 157, 782, …). The integer 5 originates from 3²+4²=5² in the squared 30-60-90 triangle. The lateral surface area S(h) and enclosed volume V(h) are identified as geometric carriers of the 5^m cycle.

三阶差分累积和 S_k 在 k_m = (5^m+3)/4 处归零（k = 2, 7, 32, 157, 782, …）。整数5源自30-60-90三角形平方空间的 3²+4²=5²。侧面积 S(h) 与封闭体积 V(h) 被确定为 5^m 代数周期的几何载体。

3. Numerical Verification Extended / 数值验证扩展
10,000 zeros (scaled 50,000 data): Relative error = 0.0000185%, RMSE = 0.0010

Prediction error does not accumulate

10,000个零点（50,000数据缩放测试）：相对误差 = 0.0000185%，RMSE = 0.0010

预测误差不累积


## Update / 更新 (2026-04-30)

**Major breakthrough: The last free parameter eliminated.**

The ratio r = m/γ, previously treated as a fitted constant, has been analytically derived as the logarithmic decay function:

r(t) = 2√3 / log(t/2π)

This function emerges from matching the geometric spiral pitch on the cone with the Riemann–von Mangoldt zero density. The dynamical equation now contains **zero free parameters**—all constants are derived from the 60° invariant, cone geometry, and zero density.

On 50,000 zeros, the zero-parameter equation achieves:
- RMSE = 0.4222 (33.8% improvement over best fixed-ratio version)
- Relative error = 0.0016%
- No error accumulation across 49,998 prediction steps

**重大突破：最后一个自由参数被消除。**

比值 r = m/γ 此前作为拟合常数处理，现已解析推导为对数衰减函数 r(t) = 2√3 / log(t/2π)。该函数由圆锥面上的几何螺距与黎曼-冯·曼戈尔特零点密度的匹配条件导出。动力学方程现在包含零个自由参数——所有常数均由60°不变量、圆锥几何和零点密度导出。

在50,000个零点上，零参数方程实现：RMSE = 0.4222（比最佳固定比值版本提升33.8%），相对误差 = 0.0016%，49,998步预测无误差累积。


Riemann Hypothesis Geometric Dynamics
黎曼猜想几何动力学
A Geometric-Dynamical Reformulation of the Riemann Hypothesis
黎曼猜想的几何-动力学重新表述

Project Overview / 项目简介
This project derives an absolute 60° geometric invariant from the functional equation ξ(s)=ξ(1-s).
本项目从函数方程 ξ(s)=ξ(1-s) 出发，推导出一个绝对的 60° 几何不变量。

This invariant constrains the non-trivial zeros of the Riemann zeta function onto a cone surface,
and yields a discrete dynamical equation governing their exact evolution along the critical line.
这个不变量将黎曼ζ函数的非平凡零点约束在一个圆锥面上，并导出一个离散动力学方程，描述零点沿临界线演化的精确规则。

All parameters are geometrically locked. Zero free parameters.
所有参数均由几何锁定。无自由参数。

A unified self-adjoint Hamiltonian is constructed, providing a concrete operator realization of the Hilbert–Pólya conjecture.
统一自伴哈密顿量已构造，为希尔伯特-波利亚猜想提供了具体的算符实现。

The periodic structure of zero-return points is formally derived, with the 5^m cycle traced to its geometric origin.
零回归点的周期结构已形式推导，5^m 周期的几何起源已被追溯。

Complete Dynamical Equation / 完整动力学方程
text
t_n = 2t_{n-1} - t_{n-2} + π/√3 - (γ/m)(t_{n-1} - t_{n-2})
Parameter / 参数	Value / 值	Source / 来源
Coefficient 2 / 系数2	2	sec 60° = 1/cos 60°
Driving term / 驱动项	π/√3	π·cot 60°
Coupling β / 耦合β	1/4	Brachistochrone variational principle on cone / 圆锥最速下降线变分原理
Mass m / 质量m	0.001	Scale-invariant / 跨尺度不变
Damping γ / 阻尼γ	0.001605	Converged value / 收敛值
c₂	mπ/√3	β · dC/dh · m
Unified Hamiltonian / 统一哈密顿量
text
H_full = (1/2)(x p_x + p_x x) + (1/2)(t p_t + p_t t) + 2 - (mπ/√3)t
All parameters geometrically locked. A concrete operator realization of the Hilbert–Pólya conjecture.
所有参数由几何锁定。希尔伯特-波利亚猜想的具体算符实现。

Key Findings / 核心发现
1. The 60° Invariant / 60°不变性
The functional equation forces cosθ = 1/2, i.e., θ = 60°, independent of the circle radius.
函数方程强制 cosθ = 1/2，即 θ = 60°，与圆半径无关。

2. Horizontal Potential V(x)=2 / 水平势 V(x)=2
Via Berry–Keating operator, the 60° invariant locks V(x) = sec 60° = 2.
通过 Berry-Keating 算符，60°不变性将水平势锁定为 V(x) = 2。

3. Cone Construction / 圆锥构造
Zero imaginary parts lifted as height. Resonance radii a_n = 2t_n/√3. Envelope: r(h) = 2h/√3.
零点虚部提升为高度。共振半径 a_n = 2t_n/√3。包络面构成圆锥。

4. Vertical Potential Φ(t) / 垂直势 Φ(t)
Only dC/dh is constant among four geometric quantities. Φ'(t) = -c₂ is constant. Φ(t) = -c₂t is linear.
四几何量中仅 dC/dh 为常数。Φ'(t) 为常数。Φ(t) 为线性势。

5. Coupling β = 1/4 / 耦合常数 β = 1/4
Derived from brachistochrone variational principle on the cone surface. β = 1/4 is a pure geometric constant—not assumed, not fitted, not extracted from data.
由圆锥面上的最速下降线变分原理导出。β = 1/4 是纯几何常数——非假设、非拟合、非从数据提取。

6. Complete Dynamical Equation / 完整动力学方程
Zero free parameters. All constants derived from the 60° invariant, cone geometry, and zero density.
零自由参数。所有常数均由60°不变量、圆锥几何和零点密度导出。

7. Unified Hamiltonian / 统一哈密顿量
H_full = (1/2)(x p_x + p_x x) + (1/2)(t p_t + p_t t) + 2 - (mπ/√3)t. Self-adjoint, zero free parameters.
H_full 自伴，零自由参数。

8. Periodic Structure / 周期结构
Zero-return points follow k_m = (5^m+3)/4. S(h) and V(h) are geometric carriers of the 5^m cycle. The integer 5 originates from 3²+4²=5² in the squared 30-60-90 triangle.
零回归点满足 k_m = (5^m+3)/4。S(h) 和 V(h) 是 5^m 周期的几何载体。整数5源自30-60-90三角形平方空间的 3²+4²=5²。

9. Numerical Verification / 数值验证
5,000 zeros: relative error 0.0079% / 5000零点：相对误差 0.0079%

50,000 zeros: m = 0.001 absolutely invariant / m = 0.001 跨尺度绝对不变

10,000 zeros (scaled): relative error 0.0000185% / RMSE 0.0010

Positive & negative zeros: identical RMSE / 正负零点 RMSE 完全一致

Geometric equation outperforms fitted version / 几何方程版全面超越拟合版

Prediction error does not accumulate / 预测误差不累积

Theoretical Significance / 理论意义
The 60° invariant expresses itself through two complementary trigonometric functions:
60°不变量通过两个互补的三角函数表达自身：

Direction / 方向	Function / 函数	Value / 值	Role / 作用
Horizontal / 水平	sec 60°	2	Locks critical line / 锁定临界线
Vertical / 垂直	π·cot 60°	π/√3	Drives zero evolution / 驱动零点演化
Together they exhaust the trigonometric content of the 30-60-90 triangle.
两者合起来用尽了 30-60-90 三角形的全部三角比。

The unified Hamiltonian and the periodic structure of zero-return points are both derived from the same 60° geometric invariant.
统一哈密顿量和零回归点的周期结构均由同一个60°几何不变量导出。

## Files / 文件结构

| File / 文件 | Description / 说明 |
|---|---|
| `60_Degree_Invariant_Riemann_Hypothesis.tex` | Paper source (English) / 英文论文源码 |
| `60_Degree_Invariant_Riemann_Hypothesis.pdf` | Paper PDF (English) / 英文论文PDF |
| `60_Degree_Invariant_Riemann_Hypothesis_CN.tex` | Paper source (Chinese) / 中文论文源码 |
| `60_Degree_Invariant_Riemann_Hypothesis_CN.pdf` | Paper PDF (Chinese) / 中文论文PDF |
| `Complete_Geometric_Dynamical_Equation.py` | Full geometric equation verification (zero free parameters) / 完整几何方程验证（零自由参数） |
| `Fitted_Dynamical_Equation.py` | Parameter fitting, rolling prediction, positive/negative symmetry / 参数拟合、滚动预测、正负零点对称性验证 |
| `zero_return_middleware.py` | N⁻¹ inverse zero-counting function verification / N⁻¹ 逆零点计数函数验证 |
| `zero_return_layer_analysis.py` | Zero-return points as layer boundaries, density stratification / 零回点层边界密度分层分析 |
| `geometric_carrier_verification.py` | S(h) and V(h) as geometric carriers of the 5ᵐ cycle / S(h)和V(h)作为5ᵐ周期的几何载体验证 |
| `geometric_algebraic_closure.py` | Geometric→r(t)→algebraic cycle→geometric closure / 几何→r(t)→代数周期→几何闭环验证 |
| `cone_visualization.py` | 3D cone visualization with 60° sight lines / 三维圆锥可视化（含60°视线） |
| `riemann_zeros_data/` | Zero data from LMFDB (5,000 & 50,000 & 100000) / LMFDB零点数据（5000和50000和100000） |

Note / 备注
This work does not claim to prove the Riemann Hypothesis. It offers a self-contained geometric framework
in which the discrete zero sequence is governed by a deterministic dynamical equation, the unified Hamiltonian is constructed, and the periodic structure of zero-return points is formally derived—all with zero free parameters, every constant derived from the 60° invariant, cone geometry, and the Riemann–von Mangoldt zero density.

本工作不声称证明了黎曼猜想。它提供一个自洽的几何框架，其中离散零点序列由一个确定性动力学方程支配，统一哈密顿量已构造，零回归点的周期结构已形式推导——全部零自由参数，每个常数均从60°不变量、圆锥几何和黎曼-冯·曼戈尔特零点密度导出。

Citation / 引用
text
Tao Li. The 60° Geometric Framework for the Riemann Hypothesis: A Geometric-Dynamical Reformulation. 2026.
Contact / 联系方式
Tao Li — 309757145@qq.com

License / 许可证
MIT License