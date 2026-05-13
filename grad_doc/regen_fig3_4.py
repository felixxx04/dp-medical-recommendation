#!/usr/bin/env python3
"""重新生成图3-4 系统总体架构图 - 清晰单向向下箭头+数据流标注"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

c = '#222222'
sbw = 2.0   # 子模块框宽
sbh = 0.55  # 子模块框高
sp = 0.25   # 同层内间距
layer_sp = 0.7  # 层之间间距 (较小, 箭头自然变短)

fig, ax = plt.subplots(figsize=(14, 11))
ax.set_xlim(0, 14)
ax.axis('off')

# 层结构定义
layers_data = [
    {'name': '表示层（前端）',
     'modules': ['React 18\n用户界面', 'TypeScript\n类型安全', 'Tailwind CSS\n样式系统', 'Vite\n构建工具']},
    {'name': '业务层（后端）',
     'modules': ['Spring Boot\nREST API', 'MyBatis\n数据持久化', 'Spring Security\nJWT认证', 'MySQL\n数据存储']},
    {'name': '算法层（模型服务）',
     'modules': ['FastAPI\n推理接口', 'DeepFM\n推荐模型', '差分隐私\n噪声机制', '安全过滤\n规则引擎']},
]

# 从上到下自动计算坐标
y_cursor = 12.5
layer_positions = []
for ld in layers_data:
    n = len(ld['modules'])
    total_w = n * sbw + (n-1) * sp
    layer_top = y_cursor
    name_h = 0.45
    mod_top = layer_top - name_h - 0.15
    mod_bot = mod_top - sbh
    layer_bot = mod_bot - 0.15
    layer_positions.append({
        'name': ld['name'], 'modules': ld['modules'],
        'layer_top': layer_top, 'layer_bot': layer_bot,
        'module_top': mod_top, 'module_bot': mod_bot,
        'total_module_w': total_w, 'n_modules': n,
    })
    y_cursor = layer_bot - layer_sp

# 大框尺寸
big_w = max(lp['total_module_w'] for lp in layer_positions) + 1.0
cx = 7.0
big_left = cx - big_w / 2

# 验证
print("坐标验证:")
for i, lp in enumerate(layer_positions):
    print(f"  层{i}: [{lp['layer_bot']:.2f}, {lp['layer_top']:.2f}]")
    if i > 0:
        gap = layer_positions[i-1]['layer_bot'] - lp['layer_top']
        print(f"    间距: {gap:.2f}")

# ===== 绘制层大框和子模块 =====
for lp in layer_positions:
    bx1, bx2 = big_left, big_left + big_w
    by1, by2 = lp['layer_bot'], lp['layer_top']
    ax.plot([bx1, bx2, bx2, bx1, bx1], [by1, by1, by2, by2, by1], color=c, lw=2.0)
    ax.text(bx1 + 0.3, by2 - 0.25, lp['name'],
            fontsize=11, fontweight='bold', color='black', va='center', ha='left')

    mleft = cx - lp['total_module_w'] / 2
    for j, mt in enumerate(lp['modules']):
        mx = mleft + j * (sbw + sp)
        mt_y = lp['module_top']
        mb_y = lp['module_bot']
        ax.plot([mx, mx+sbw, mx+sbw, mx, mx], [mb_y, mb_y, mt_y, mt_y, mb_y], color=c, lw=1.2)
        ax.text(mx + sbw/2, (mt_y+mb_y)/2, mt, ha='center', va='center',
                fontsize=9, color='black', linespacing=1.2)

# ===== 层间连接箭头 (单向向下+标注) =====
al = 0.12  # 箭头三角高度
arrow_labels = ['REST API / JSON', '/model/predict']

for i in range(len(layer_positions) - 1):
    from_bot = layer_positions[i]['layer_bot']
    to_top = layer_positions[i+1]['layer_top']
    mid_y = (from_bot + to_top) / 2

    # 向下箭头线: 从上层底边到下层顶边
    ax.plot([cx, cx], [from_bot, to_top + al], color=c, lw=1.5)
    # 向下三角 (尖端在下层顶边)
    ax.plot([cx, cx-0.1, cx+0.1, cx],
            [to_top, to_top+al, to_top+al, to_top], color=c, lw=1.5)

    # 标注 (箭头右侧)
    ax.text(cx + 0.5, mid_y, arrow_labels[i],
            fontsize=9, color='black', ha='left', va='center')

# ===== 用户框 (最上方) =====
user_gap = 0.5
user_w = 2.0
user_h = 0.5
user_bot = layer_positions[0]['layer_top'] + user_gap
user_top = user_bot + user_h

ax.set_ylim(layer_positions[-1]['layer_bot'] - 0.5, user_top + 0.5)

# 用户框
ux1, ux2 = cx - user_w/2, cx + user_w/2
ax.plot([ux1, ux2, ux2, ux1, ux1], [user_bot, user_bot, user_top, user_top, user_bot], color=c, lw=1.5)
ax.text(cx, (user_top+user_bot)/2, '用户',
        ha='center', va='center', fontsize=10, fontweight='bold', color='black')

# 用户→表示层 向下箭头 (只触碰框边)
ax.plot([cx, cx], [user_bot, layer_positions[0]['layer_top'] + al], color=c, lw=1.5)
ax.plot([cx, cx-0.1, cx+0.1, cx],
        [layer_positions[0]['layer_top'],
         layer_positions[0]['layer_top'] + al,
         layer_positions[0]['layer_top'] + al,
         layer_positions[0]['layer_top']],
        color=c, lw=1.5)

plt.savefig('D:/grad_medical/grad_doc/charts/fig_3_4_system_architecture_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图3-4已重新生成: 单向箭头+数据流标注')