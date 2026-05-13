#!/usr/bin/env python3
"""重新生成图1-1 论文技术路线图 - 黑白配色, 修复重叠和样式不一致问题"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(18, 10))
ax.set_xlim(0, 18)
ax.set_ylim(0, 10)
ax.axis('off')

# 黑白配色方案
row_label_bg = '#F0F0F0'  # 行标签浅灰背景
box_border = '#333333'    # 边框深灰
text_color = '#000000'    # 黑色文字
arrow_color = '#333333'   # 箭头深灰

# 三行数据
rows = [
    {'label': '研究内容', 'items': [
        '差分隐私理论\n(定义、机制、预算)',
        '深度学习推荐算法\n(FM→DeepFM→注意力)',
        '三层安全架构\n(安全过滤→规则标记→DP排序)',
        '隐私效用权衡\n(ε-效用分析、临床阈值)'
    ]},
    {'label': '研究方法', 'items': [
        '文献调研与\n理论分析',
        '模型设计与\n实验验证',
        '规则引擎与\n系统集成',
        '对比实验与\n效果评估'
    ]},
    {'label': '预期成果', 'items': [
        '差分隐私保护\n机制设计',
        'DeepFM推荐\n模型实现',
        '智能用药推荐\n系统开发',
        '隐私-效用\n权衡验证'
    ]},
]

box_w = 3.0
box_h = 1.6
label_w = 2.2
label_h = 1.6
gap_x = 0.5  # 水平间距
gap_y = 0.6  # 垂直间距
start_x = 0.3 + label_w + gap_x  # 内容框紧跟标签框后面
start_y = 9.0

for r_idx, row in enumerate(rows):
    y = start_y - r_idx * (box_h + gap_y)

    # 行标签框 - 单独放置，不与内容框重叠
    label_x = 0.3
    label_box = FancyBboxPatch(
        (label_x, y - label_h), label_w, label_h,
        boxstyle="round,pad=0.15",
        facecolor=row_label_bg, edgecolor=box_border, linewidth=1.5
    )
    ax.add_patch(label_box)
    ax.text(label_x + label_w/2, y - label_h/2, row['label'],
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=text_color)

    # 内容框
    for c_idx, item in enumerate(row['items']):
        x = start_x + c_idx * (box_w + gap_x)
        content_box = FancyBboxPatch(
            (x, y - box_h), box_w, box_h,
            boxstyle="round,pad=0.12",
            facecolor='white', edgecolor=box_border, linewidth=1.2
        )
        ax.add_patch(content_box)
        ax.text(x + box_w/2, y - box_h/2, item,
                ha='center', va='center', fontsize=10,
                color=text_color, linespacing=1.4)

        # 同行内水平箭头 - 放在框之间的间隙中
        if c_idx < len(row['items']) - 1:
            next_x = start_x + (c_idx + 1) * (box_w + gap_x)
            arrow_start_x = x + box_w + 0.05   # 当前框右边缘外
            arrow_end_x = next_x - 0.05         # 下一个框左边缘外
            ax.annotate('', xy=(arrow_end_x, y - box_h/2),
                       xytext=(arrow_start_x, y - box_h/2),
                       arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.5))

    # 垂直箭头（连接到下一行对应列）- 放在框之间的间隙中
    if r_idx < len(rows) - 1:
        next_y = start_y - (r_idx + 1) * (box_h + gap_y)
        mid_x = start_x + box_w/2
        arrow_start_y = y - box_h - 0.05   # 当前框下边缘外
        arrow_end_y = next_y + 0.05         # 下一个框上边缘外
        ax.annotate('', xy=(mid_x, arrow_end_y),
                   xytext=(mid_x, arrow_start_y),
                   arrowprops=dict(arrowstyle='->', color=arrow_color, lw=1.5))

# 顶部标题
ax.text(9, 9.7, '论文技术路线', ha='center', va='center',
        fontsize=14, fontweight='bold', color=text_color)

plt.tight_layout()
plt.savefig('D:/grad_medical/grad_doc/charts/fig_1_1_technical_roadmap_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图1-1已重新生成: fig_1_1_technical_roadmap_v2.png')