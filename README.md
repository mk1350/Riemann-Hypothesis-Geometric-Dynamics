# Riemann Hypothesis Geometric Dynamics
# 黎曼猜想几何动力学

**A Geometric-Dynamical Reformulation of the Riemann Hypothesis**
**黎曼猜想的几何-动力学重新表述**

---

## Project Overview / 项目简介

This project derives an absolute 60° geometric invariant from the functional equation ξ(s)=ξ(1-s).
本项目从函数方程 ξ(s)=ξ(1-s) 出发，推导出一个绝对的 60° 几何不变量。

This invariant constrains the non-trivial zeros of the Riemann zeta function onto a cone surface,
and yields a discrete dynamical equation governing their exact evolution along the critical line.
这个不变量将黎曼ζ函数的非平凡零点约束在一个圆锥面上，并导出一个离散动力学方程，描述零点沿临界线演化的精确规则。

All parameters are locked by geometry. Zero free parameters.
所有参数均由几何锁定。无自由参数。

---

## Complete Dynamical Equation / 完整动力学方程
t_n = 2t_{n-1} - t_{n-2} + π/√3 - (γ/m)(t_{n-1} - t_{n-2})

text

| Parameter / 参数 | Value / 值 | Source / 来源 |
|---|---|---|
| Coefficient 2 / 系数2 | 2 | sec 60° = 1/cos 60° |
| Driving term / 驱动项 | π/√3 | π·cot 60° |
| Coupling β / 耦合β | 1/4 | Brachistochrone on cone / 圆锥最速下降线 |
| Mass m / 质量m | 0.001 | Scale-invariant / 跨尺度不变 |
| Damping γ / 阻尼γ | 0.001605 | Converged value / 收敛值 |
| c₂ | mπ/√3 | β · dC/dh · m |

---

## Key Findings / 核心发现

### 1. The 60° Invariant / 60°不变性
The functional equation forces cosθ = 1/2, i.e., θ = 60°, independent of the circle radius.
函数方程强制 cosθ = 1/2，即 θ = 60°，与圆半径无关。

### 2. Horizontal Potential V(x)=2 / 水平势 V(x)=2
Via Berry–Keating operator, the 60° invariant locks V(x) = sec 60° = 2.
通过 Berry-Keating 算符，60°不变性将水平势锁定为 V(x) = 2。

### 3. Cone Construction / 圆锥构造
Zero imaginary parts lifted as height. Resonance radii a_n = 2t_n/√3. Envelope: r(h) = 2h/√3.
零点虚部提升为高度。共振半径 a_n = 2t_n/√3。包络面构成圆锥。

### 4. Vertical Potential Φ(t) / 垂直势 Φ(t)
Only dC/dh is constant among four geometric quantities. Φ'(t) = -c₂ is constant. Φ(t) = -c₂t is linear.
四几何量中仅 dC/dh 为常数。Φ'(t) 为常数。Φ(t) 为线性势。

### 5. Coupling β = 1/4 / 耦合常数 β = 1/4
Derived from brachistochrone principle via twofold force decomposition on the cone.
通过圆锥面上最速下降线的两次力分解导出。

### 6. Numerical Verification / 数值验证
- 5,000 zeros: relative error 0.0079% / 5000零点：相对误差 0.0079%
- 50,000 zeros: m = 0.001 absolutely invariant / m = 0.001 跨尺度绝对不变
- Positive & negative zeros: identical RMSE / 正负零点 RMSE 完全一致
- Geometric equation outperforms fitted version / 几何方程版全面超越拟合版

---

## Theoretical Significance / 理论意义

The 60° invariant expresses itself through two complementary trigonometric functions:
60°不变量通过两个互补的三角函数表达自身：

| Direction / 方向 | Function / 函数 | Value / 值 | Role / 作用 |
|---|---|---|---|
| Horizontal / 水平 | sec 60° | 2 | Locks critical line / 锁定临界线 |
| Vertical / 垂直 | π·cot 60° | π/√3 | Drives zero evolution / 驱动零点演化 |

Together they exhaust the trigonometric content of the 30-60-90 triangle.
两者合起来用尽了 30-60-90 三角形的全部三角比。

---

## Files / 文件结构

| File / 文件 | Description / 说明 |
|---|---|
| `60_Degree_Invariant_Riemann_Hypothesis.tex` | Paper source (English) / 英文论文源码 |
| `60_Degree_Invariant_Riemann_Hypothesis.pdf` | Paper PDF (English) / 英文论文PDF |
| `Riemann_Hypothesis_60_Degree_CN.tex` | Paper source (Chinese) / 中文论文源码 |
| `Fitted_Dynamical_Equation.py` | Parameter fitting & rolling prediction / 参数拟合与滚动预测 |
| `Complete_Geometric_Dynamical_Equation.py` | Full geometric equation verification / 完整几何方程验证 |
| `cone_visualization.py` | 3D cone visualization / 三维圆锥可视化 |
| `riemann_zeros_data/` | Zero data from LMFDB (5,000 & 50,000) / LMFDB零点数据 |

---

## Note / 备注

This work does not claim to prove the Riemann Hypothesis. It offers a self-contained geometric framework
in which the discrete zero sequence is governed by a deterministic dynamical equation whose every
parameter is derived from first geometric principles.

本工作不声称证明了黎曼猜想。它提供一个自洽的几何框架，其中离散零点序列由一个确定性动力学方程
支配，该方程的每个参数均从第一几何原理导出。

---

## Citation / 引用
Tao Li. The 60° Geometric Framework for the Riemann Hypothesis: A Geometric-Dynamical Reformulation. 2026.

text

---

## Contact / 联系方式

Tao Li — 309757145@qq.com

## License / 许可证

MIT License
