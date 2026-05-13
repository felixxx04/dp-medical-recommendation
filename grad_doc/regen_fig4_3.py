#!/usr/bin/env python3
"""重新生成图4-3 用药推荐流程图 - 黑白配色, 两列布局, 箭头只触碰框边"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

c = '#222222'
al = 0.1

fig, ax = plt.subplots(figsize=(14, 11))
ax.set_xlim(0, 14)
ax.set_ylim(0, 14)
ax.axis('off')

# ===== 两列布局 =====
# 左列: 数据准备阶段 (x center = 3.5)
# 右列: 安全过滤+推荐排序 (x center = 10.5)
# 水平连接箭头在中间 (x = 7.0)

lx_c = 3.5   # 左列中心x
rx_c = 10.5  # 右列中心x
box_w = 5.0
pitch = 0.55  # 框+间距

# ===== 左列：数据准备 =====
left_steps = [
    ('获取患者信息', ['基本信息、疾病史、过敏史', '当前用药、V2生理指标']),
    ('疾病名称映射', ['DiseaseMapper中→英编码', 'SEMANTIC_VOCAB_MAP匹配']),
    ('药物候选检索', ['从1815种药物中检索', '基于适应症匹配筛选']),
]

left_positions = []
y = 12.5
for name, desc in left_steps:
    h = 0.65 if len(desc) <= 2 else 0.8
    left_positions.append({'name': name, 'desc': desc, 'top': y, 'bot': y - h, 'cx': lx_c, 'w': box_w})
    y = y - h - pitch

# 左列标题
left_title_y = 13.2
ax.text(lx_c, left_title_y, '数据准备阶段',
        ha='center', va='center', fontsize=12, fontweight='bold', color='black')

# ===== 右列：安全+排序 =====
right_steps = [
    ('SafetyFilter 安全过滤', ['绝对禁忌症排除', '过敏冲突排除', '重大药物交互排除', '妊娠X类/儿科禁忌排除']),
    ('RuleMarker 规则标记', ['相对禁忌警告', '中等交互标记', '妊娠C/D类标记', '添加审查标记（不排除）']),
    ('DeepFM 个性化评分', ['嵌入层+FM+Deep推理', '仅对安全候选评分']),
    ('差分隐私噪声注入', ['Laplace/Gaussian噪声', 'ε预算消耗追踪', '临床阈值后处理']),
]

right_positions = []
y = 12.5
for name, desc in right_steps:
    h = 0.65 if len(desc) <= 2 else 0.9
    right_positions.append({'name': name, 'desc': desc, 'top': y, 'bot': y - h, 'cx': rx_c, 'w': box_w})
    y = y - h - pitch

right_title_y = 13.2
ax.text(rx_c, right_title_y, '安全过滤与推荐排序阶段',
        ha='center', va='center', fontsize=12, fontweight='bold', color='black')

# ===== 输出框 =====
out_y_top = min(right_positions[-1]['bot'], left_positions[-1]['bot']) - 0.4
out_y_bot = out_y_top - 0.7
out_cx = 7.0
out_w = 3.0
ol, or_ = out_cx - out_w/2, out_cx + out_w/2
ax.plot([ol, or_, or_, ol, ol],
        [out_y_bot, out_y_bot, out_y_top, out_y_top, out_y_bot], color=c, lw=2.0)
ax.text(out_cx, (out_y_top + out_y_bot)/2, '安全推荐结果\n(隐私保护输出)',
        ha='center', va='center', fontsize=11, fontweight='bold', color='black', linespacing=1.3)

# ===== 绘制左列框 =====
for lp in left_positions:
    lx = lp['cx'] - lp['w']/2
    rx = lp['cx'] + lp['w']/2
    ty, by = lp['top'], lp['bot']
    ax.plot([lx, rx, rx, lx, lx], [by, by, ty, ty, by], color=c, lw=1.5)
    # 步骤名称
    ax.text(lp['cx'], ty - 0.2, lp['name'],
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='black')
    # 分隔线
    ax.plot([lx + 0.2, rx - 0.2], [ty - 0.38, ty - 0.38], color=c, lw=0.6)
    # 描述
    for j, d in enumerate(lp['desc']):
        dy = ty - 0.38 - 0.2 - j * 0.22
        ax.text(lp['cx'], dy, d,
                ha='center', va='center', fontsize=7.5, color='#333333')

# ===== 绘制右列框 =====
for rp in right_positions:
    lx = rp['cx'] - rp['w']/2
    rx = rp['cx'] + rp['w']/2
    ty, by = rp['top'], rp['bot']
    ax.plot([lx, rx, rx, lx, lx], [by, by, ty, ty, by], color=c, lw=1.5)
    ax.text(rp['cx'], ty - 0.2, rp['name'],
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='black')
    ax.plot([lx + 0.2, rx - 0.2], [ty - 0.38, ty - 0.38], color=c, lw=0.6)
    for j, d in enumerate(rp['desc']):
        dy = ty - 0.38 - 0.2 - j * 0.22
        ax.text(rp['cx'], dy, d,
                ha='center', va='center', fontsize=7.5, color='#333333')

# ===== 左列内垂直箭头 =====
for i in range(len(left_positions) - 1):
    from_bot = left_positions[i]['bot']
    to_top = left_positions[i+1]['top']
    ax.plot([lx_c, lx_c], [from_bot, to_top + al], color=c, lw=1.2)
    ax.plot([lx_c, lx_c - 0.08, lx_c + 0.08, lx_c],
            [to_top, to_top + al, to_top + al, to_top], color=c, lw=1.2)

# ===== 右列内垂直箭头 =====
for i in range(len(right_positions) - 1):
    from_bot = right_positions[i]['bot']
    to_top = right_positions[i+1]['top']
    ax.plot([rx_c, rx_c], [from_bot, to_top + al], color=c, lw=1.2)
    ax.plot([rx_c, rx_c - 0.08, rx_c + 0.08, rx_c],
            [to_top, to_top + al, to_top + al, to_top], color=c, lw=1.2)

# ===== 左列→右列 水平连接箭头 =====
# 左列最后一框 → 右列第一框
l_last = left_positions[-1]
r_first = right_positions[0]
l_mid_y = (l_last['top'] + l_last['bot']) / 2
r_mid_y = (r_first['top'] + r_first['bot']) / 2
conn_y = (l_mid_y + r_mid_y) / 2
# 水平线: 从左列右边到右列左边
from_x = lx_c + box_w/2
to_x = rx_c - box_w/2
ax.plot([from_x, to_x - al], [l_mid_y, r_mid_y], color=c, lw=1.3)
ax.plot([to_x - al, to_x, to_x - al],
        [r_mid_y + 0.08, r_mid_y, r_mid_y - 0.08], color=c, lw=1.3)
ax.text((from_x + to_x)/2, l_mid_y + 0.25, '候选药物集', fontsize=8, color='black', ha='center')

# ===== 左右列到输出框 =====
# 左列最后框到输出
l_last_bot = left_positions[-1]['bot']
l_to_out = (l_last_bot + out_y_top) / 2
ax.plot([lx_c, lx_c], [l_last_bot, out_y_top + al], color=c, lw=1.3)
ax.plot([lx_c, lx_c - 0.08, lx_c + 0.08, lx_c],
        [out_y_top, out_y_top + al, out_y_top + al, out_y_top], color=c, lw=1.3)

# 右列最后框到输出
r_last_bot = right_positions[-1]['bot']
r_to_out = (r_last_bot + out_y_top) / 2
ax.plot([rx_c, rx_c], [r_last_bot, out_y_top + al], color=c, lw=1.3)
ax.plot([rx_c, rx_c - 0.08, rx_c + 0.08, rx_c],
        [out_y_top, out_y_top + al, out_y_top + al, out_y_top], color=c, lw=1.3)

# 阶段标签
ax.text(lx_c, l_last['bot'] - 0.05, '汇总输出',
        ha='center', va='top', fontsize=8, color='#444444')
ax.text(rx_c, right_positions[-1]['bot'] - 0.05, '安全+排序完成',
        ha='center', va='top', fontsize=8, color='#444444')

plt.savefig('D:/grad_medical/grad_doc/charts/fig_4_3_recommendation_flow_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图4-3已重新生成')
