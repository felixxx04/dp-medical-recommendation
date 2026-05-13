#!/usr/bin/env python3
"""重新生成图3-5 系统功能结构图 - 标准层级树形结构, 答辩清晰"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

c = '#222222'

# 模块数据: 名称 + 子功能列表
modules = [
    {'name': '用户认证模块', 'funcs': ['登录认证', 'JWT令牌管理', '权限控制']},
    {'name': '患者管理模块', 'funcs': ['基本信息管理', '健康档案', '生理指标记录']},
    {'name': '用药推荐模块', 'funcs': ['DeepFM推荐引擎', '三层安全过滤', '差分隐私保护']},
    {'name': '隐私管理模块', 'funcs': ['隐私参数配置', '预算追踪审计', '隐私事件日志']},
    {'name': '系统管理模块', 'funcs': ['药物数据维护', '用户账号管理', '系统参数配置']},
]

# 布局参数
cw = 16   # 画布逻辑宽度
root_w = 5.0
root_h = 0.8
mod_w = 2.6
mod_h = 1.8
mod_gap = 0.5
n = len(modules)

# 自动计算坐标
total_mod_w = n * mod_w + (n - 1) * mod_gap
mod_start_x = (cw - total_mod_w) / 2

root_cx = cw / 2
root_top = 8.5
root_bot = root_top - root_h

gap = 0.7
mod_top = root_bot - gap
mod_bot = mod_top - mod_h

# 各模块中心x
mod_cx = []
for i in range(n):
    left = mod_start_x + i * (mod_w + mod_gap)
    mod_cx.append(left + mod_w / 2)

# bus线y (根底边与模块顶边之间的中点)
bus_y = (root_bot + mod_top) / 2

# 验证间距
print(f"Root: [{root_bot:.2f}, {root_top:.2f}]")
print(f"Modules: [{mod_bot:.2f}, {mod_top:.2f}]")
print(f"Gap root→modules: {root_bot - mod_top:.2f}")

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, cw)
ax.set_ylim(mod_bot - 0.5, root_top + 0.5)
ax.axis('off')

# ===== 绘制根框 =====
rx1 = root_cx - root_w/2
rx2 = root_cx + root_w/2
ax.plot([rx1, rx2, rx2, rx1, rx1], [root_bot, root_bot, root_top, root_top, root_bot], color=c, lw=2.0)
ax.text(root_cx, (root_top + root_bot)/2, '智能用药推荐系统',
        ha='center', va='center', fontsize=12, fontweight='bold', color='black')

# ===== 绘制模块框 =====
for i, mod in enumerate(modules):
    cx = mod_cx[i]
    xl = cx - mod_w/2
    xr = cx + mod_w/2

    # 外框
    ax.plot([xl, xr, xr, xl, xl], [mod_bot, mod_bot, mod_top, mod_top, mod_bot], color=c, lw=1.5)

    # 模块名称 (框顶部居中, 粗体)
    name_y = mod_top - 0.3
    ax.text(cx, name_y, mod['name'],
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='black')

    # 分隔线 (名称与子功能之间)
    sep_y = name_y - 0.3
    ax.plot([xl + 0.2, xr - 0.2], [sep_y, sep_y], color=c, lw=0.8)

    # 子功能列表 (分隔线下方, 小字)
    func_start_y = sep_y - 0.3
    for j, func in enumerate(mod['funcs']):
        func_y = func_start_y - j * 0.38
        ax.text(cx, func_y, func,
                ha='center', va='center', fontsize=8, color='#333333')

# ===== 绘制连接线 (bus总线风格) =====
# 根底边 → bus线 (垂直线)
ax.plot([root_cx, root_cx], [root_bot, bus_y], color=c, lw=1.5)

# bus横线 (连接所有模块中心)
ax.plot([mod_cx[0], mod_cx[-1]], [bus_y, bus_y], color=c, lw=1.5)

# bus → 各模块顶边 (垂直线+箭头)
al = 0.12  # 箭头三角高度
for cx in mod_cx:
    # 垂直线到模块顶边
    ax.plot([cx, cx], [bus_y, mod_top + al], color=c, lw=1.3)
    # 箭头三角 (指向模块顶边)
    ax.plot([cx, cx-0.1, cx+0.1, cx],
            [mod_top, mod_top+al, mod_top+al, mod_top], color=c, lw=1.3)

# 根底边箭头 (指向bus方向)
ax.plot([root_cx, root_cx-0.1, root_cx+0.1, root_cx],
        [bus_y, bus_y+al, bus_y+al, bus_y], color=c, lw=1.3)

plt.savefig('D:/grad_medical/grad_doc/charts/fig_3_5_function_structure_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图3-5已重新生成: fig_3_5_function_structure_v2.png')