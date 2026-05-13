#!/usr/bin/env python3
"""重新生成图4-1 三层推荐安全架构图 - 文本不溢出/箭头减半/间距紧凑"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

c = '#222222'

# 布局参数
cx = 6.0        # 中心x
inout_w = 3.8   # 输入/输出框宽度
layer_w = 7.6   # 层框宽度 (加宽防溢出)
inout_h = 0.55  # 输入/输出框高度
sp = 0.35       # 框之间间距 (缩小为原来一半)
al = 0.10       # 箭头三角高度

# 各层框高度 (根据内容精确计算)
sf_h = 2.05     # SafetyFilter (5条功能)
rm_h = 1.8      # RuleMarker (4条功能)
df_h = 1.8      # DeepFM+DP (4条功能)

y = 13.8  # 起始顶部
positions = []

# 输入框
positions.append({'name': '全部药物候选\n(1815种)', 'top': y, 'bot': y - inout_h,
                  'cx': cx, 'w': inout_w, 'type': 'inout'})
y = positions[-1]['bot'] - sp

# SafetyFilter
positions.append({'name': '第一层：安全过滤 (SafetyFilter)',
                  'desc': '确定性硬排除 — DP噪声不影响此层',
                  'items': ['绝对禁忌症排除', '过敏冲突排除', '重大药物交互排除', '妊娠X类排除', '儿科禁忌排除'],
                  'top': y, 'bot': y - sf_h, 'cx': cx, 'w': layer_w, 'type': 'layer'})
y = positions[-1]['bot'] - sp

# RuleMarker
positions.append({'name': '第二层：规则标记 (RuleMarker)',
                  'desc': '软标记（不排除）— 添加审查标记',
                  'items': ['相对禁忌警告', '中等交互标记', '妊娠C/D类标记', '用药剂量调整提示'],
                  'top': y, 'bot': y - rm_h, 'cx': cx, 'w': layer_w, 'type': 'layer'})
y = positions[-1]['bot'] - sp

# DeepFM+DP
positions.append({'name': '第三层：推荐排序 (DeepFM+差分隐私)',
                  'desc': '个性化评分 — 仅此层应用DP噪声',
                  'items': ['DeepFM推理评分', '差分隐私噪声注入', '临床阈值后处理', '置信区间计算'],
                  'top': y, 'bot': y - df_h, 'cx': cx, 'w': layer_w, 'type': 'layer'})
y = positions[-1]['bot'] - sp

# 输出框
positions.append({'name': '安全推荐结果\n(隐私保护)', 'top': y, 'bot': y - inout_h,
                  'cx': cx, 'w': inout_w, 'type': 'inout'})

print("坐标验证:")
for i, p in enumerate(positions):
    print(f"  [{p['bot']:.2f}, {p['top']:.2f}] {p['type']}: {p['name'][:20]}")
    if i > 0:
        gap = positions[i-1]['bot'] - p['top']
        print(f"    间距: {gap:.2f}")

fig, ax = plt.subplots(figsize=(12, 12))
fig_bot = positions[-1]['bot'] - 0.4
fig_top = positions[0]['top'] + 0.4
ax.set_xlim(0, 12)
ax.set_ylim(fig_bot, fig_top)
ax.axis('off')

# 输入/输出框
for p in positions:
    if p['type'] != 'inout':
        continue
    lx = p['cx'] - p['w'] / 2
    rx = p['cx'] + p['w'] / 2
    ax.plot([lx, rx, rx, lx, lx], [p['bot'], p['bot'], p['top'], p['top'], p['bot']], color=c, lw=2.0)
    ax.text(p['cx'], (p['top'] + p['bot']) / 2, p['name'],
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='black', linespacing=1.3)

# 层框
for p in positions:
    if p['type'] != 'layer':
        continue
    lx = p['cx'] - p['w'] / 2
    rx = p['cx'] + p['w'] / 2
    ty, by = p['top'], p['bot']

    # 外框
    ax.plot([lx, rx, rx, lx, lx], [by, by, ty, ty, by], color=c, lw=1.8)

    # 层标题 (紧凑间距)
    title_y = ty - 0.28
    ax.text(p['cx'], title_y, p['name'],
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='black')

    # 描述文字
    desc_y = title_y - 0.25
    ax.text(p['cx'], desc_y, p['desc'],
            ha='center', va='center', fontsize=8.5, color='#444444')

    # 分隔线
    sep_y = desc_y - 0.12
    ax.plot([lx + 0.3, rx - 0.3], [sep_y, sep_y], color=c, lw=0.7)

    # 功能列表 (紧凑间距)
    item_start_y = sep_y - 0.18
    for j, item in enumerate(p['items']):
        iy = item_start_y - j * 0.22
        ax.text(lx + 0.5, iy, '- ' + item,
                ha='left', va='center', fontsize=8.5, color='black')

# 层间连接箭头 (短箭头, 只碰框边)
flow_labels = ['药物候选集', '安全候选集', '标记候选集', '评分结果']

for i in range(len(positions) - 1):
    from_bot = positions[i]['bot']
    to_top = positions[i+1]['top']
    mid_y = (from_bot + to_top) / 2

    # 垂直线: 从上层底边到下层顶边+三角底
    ax.plot([cx, cx], [from_bot, to_top + al], color=c, lw=1.5)
    # 向下三角 (尖端在下层顶边)
    ax.plot([cx, cx - 0.08, cx + 0.08, cx],
            [to_top, to_top + al, to_top + al, to_top], color=c, lw=1.5)

    # 数据流标注 (右侧)
    ax.text(cx + 0.9, mid_y, flow_labels[i],
            fontsize=8.5, color='black', ha='left', va='center')

plt.savefig('D:/grad_medical/grad_doc/charts/fig_4_1_three_layer_architecture_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图4-1已重新生成')
