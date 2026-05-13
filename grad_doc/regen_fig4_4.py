#!/usr/bin/env python3
"""重新生成图4-4 隐私保护推理流程图 - 水平管道式布局, 黑白配色, 箭头只触碰框边"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

c = '#222222'
al = 0.1   # 箭头三角高度

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# ===== 水平管道式布局 =====
# 主流程水平排列，每个阶段是一个管道节点
# 隐私预算管理作为底部横跨的监督层

stages = [
    {'name': '接收请求', 'xy': (1.5, 6.0), 'w': 2.2, 'h': 1.8,
     'lines': ['患者ID、疾病信息', '推荐参数获取', '用户身份验证']},
    {'name': '隐私预算检查', 'xy': (5.0, 6.0), 'w': 2.6, 'h': 1.8,
     'lines': ['查询剩余ε预算', '预算充足→继续', '预算不足→拒绝/降级']},
    {'name': '安全过滤层', 'xy': (8.8, 6.0), 'w': 2.4, 'h': 1.8,
     'lines': ['禁忌症/过敏排除', '(无DP噪声)', '确定性硬排除']},
    {'name': 'DeepFM推理+DP', 'xy': (12.2, 6.0), 'w': 2.5, 'h': 1.8,
     'lines': ['模型前向推理', 'Laplace/Gaussian噪声', '尺度=Δf/ε']},
]

# ===== 后处理阶段（下方） =====
post_stages = [
    {'name': '临床阈值后处理', 'xy': (5.0, 3.0), 'w': 2.6, 'h': 1.5,
     'lines': ['得分<0.15 → 置零', '(DP后处理定理)', 'min(1.0, raw+0.35)上限']},
    {'name': '预算扣减与审计', 'xy': (8.8, 3.0), 'w': 2.4, 'h': 1.5,
     'lines': ['ε消耗记录', 'privacy_ledger写入', '审计日志持久化']},
    {'name': '返回结果', 'xy': (12.2, 3.0), 'w': 2.5, 'h': 1.5,
     'lines': ['排序推荐列表', '置信区间(95% CI)', 'dpAnomaly异常标记']},
]

# ===== 绘制主流程管道节点 =====
for s in stages:
    x, y = s['xy']
    w, h = s['w'], s['h']
    ax.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], color=c, lw=1.8)
    ax.text(x + w/2, y + h - 0.25, s['name'],
            ha='center', va='center', fontsize=10, fontweight='bold', color='black')
    ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.48, y + h - 0.48], color=c, lw=0.6)
    for j, line in enumerate(s['lines']):
        ly = y + h - 0.48 - 0.2 - j * 0.26
        ax.text(x + w/2, ly, line,
                ha='center', va='center', fontsize=8, color='#333333')

# ===== 绘制后处理节点 =====
for s in post_stages:
    x, y = s['xy']
    w, h = s['w'], s['h']
    ax.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], color=c, lw=1.5)
    ax.text(x + w/2, y + h - 0.25, s['name'],
            ha='center', va='center', fontsize=10, fontweight='bold', color='black')
    ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.45, y + h - 0.45], color=c, lw=0.6)
    for j, line in enumerate(s['lines']):
        ly = y + h - 0.45 - 0.18 - j * 0.26
        ax.text(x + w/2, ly, line,
                ha='center', va='center', fontsize=7.5, color='#333333')

# ===== 主流程水平箭头 =====
for i in range(len(stages) - 1):
    from_x = stages[i]['xy'][0] + stages[i]['w']
    from_y = stages[i]['xy'][1] + stages[i]['h'] / 2
    to_x = stages[i+1]['xy'][0]
    to_y = stages[i+1]['xy'][1] + stages[i+1]['h'] / 2
    ax.plot([from_x, to_x - al], [from_y, to_y], color=c, lw=1.5)
    ax.plot([to_x - al, to_x, to_x - al],
            [to_y + 0.08, to_y, to_y - 0.08], color=c, lw=1.5)

# ===== 后处理水平箭头 =====
for i in range(len(post_stages) - 1):
    from_x = post_stages[i]['xy'][0] + post_stages[i]['w']
    from_y = post_stages[i]['xy'][1] + post_stages[i]['h'] / 2
    to_x = post_stages[i+1]['xy'][0]
    to_y = post_stages[i+1]['xy'][1] + post_stages[i+1]['h'] / 2
    ax.plot([from_x, to_x - al], [from_y, to_y], color=c, lw=1.3)
    ax.plot([to_x - al, to_x, to_x - al],
            [to_y + 0.08, to_y, to_y - 0.08], color=c, lw=1.3)

# ===== 主流程→后处理 垂直箭头 =====
# DeepFM+DP (stage 3) bottom → 临床阈值后处理 top
s3 = stages[3]
ps0 = post_stages[0]
s3_bot_x = s3['xy'][0] + s3['w'] / 2
s3_bot_y = s3['xy'][1]
ps0_top_x = ps0['xy'][0] + ps0['w'] / 2
ps0_top_y = ps0['xy'][1] + ps0['h']
ax.plot([s3_bot_x, ps0_top_x], [s3_bot_y - al, ps0_top_y + al], color=c, lw=1.3)
ax.plot([ps0_top_x, ps0_top_x - 0.08, ps0_top_x + 0.08, ps0_top_x],
        [ps0_top_y, ps0_top_y + al, ps0_top_y + al, ps0_top_y], color=c, lw=1.3)
ax.text((s3_bot_x + ps0_top_x)/2 + 0.3, (s3_bot_y + ps0_top_y)/2,
        '噪声评分', fontsize=8, color='black', ha='left', va='center')

# 安全过滤层 bottom → 预算扣减 (连接线示意无需DP的路径)
s2 = stages[2]
ps1 = post_stages[1]
s2_bot_x = s2['xy'][0] + s2['w'] / 2
s2_bot_y = s2['xy'][1]
ps1_top_x = ps1['xy'][0] + ps1['w'] / 2
ps1_top_y = ps1['xy'][1] + ps1['h']
# Dashed line: safety filter doesn't use DP, but results feed into audit
ax.plot([s2_bot_x, ps1_top_x], [s2_bot_y - al, ps1_top_y + al], color=c, lw=1.0, linestyle='--')
ax.text((s2_bot_x + ps1_top_x)/2 - 0.3, (s2_bot_y + ps1_top_y)/2,
        '过滤计数', fontsize=8, color='#666666', ha='right', va='center')

# ===== 隐私预算监督层 (底部横条) =====
privacy_bar_y = 1.2
privacy_bar_h = 0.6
bar_l, bar_r = 1.5, 14.7
ax.plot([bar_l, bar_r, bar_r, bar_l, bar_l],
        [privacy_bar_y, privacy_bar_y, privacy_bar_y + privacy_bar_h, privacy_bar_y + privacy_bar_h, privacy_bar_y],
        color=c, lw=2.0, linestyle='--')
ax.text(8.1, privacy_bar_y + privacy_bar_h/2,
        '隐私预算全局管理：隐私配置(ε,δ) → 强组合定理累计 → 预算用尽自动拒绝 → 定期重置',
        ha='center', va='center', fontsize=9, color='black')

# 预算检查 → 预算条
s1_bot = stages[1]['xy'][0] + stages[1]['w'] / 2
s1_y = stages[1]['xy'][1]
bar_top = privacy_bar_y + privacy_bar_h
ax.plot([s1_bot, s1_bot], [s1_y, bar_top + al], color=c, lw=1.0, linestyle=':')
ax.plot([s1_bot, s1_bot - 0.08, s1_bot + 0.08, s1_bot],
        [bar_top, bar_top + al, bar_top + al, bar_top], color=c, lw=1.0)

# 预算扣减 → 预算条
ps1_bot = post_stages[1]['xy'][0] + post_stages[1]['w'] / 2
ps1_y = post_stages[1]['xy'][1]
ax.plot([ps1_bot, ps1_bot], [ps1_y, bar_top + al], color=c, lw=1.0, linestyle=':')
ax.plot([ps1_bot, ps1_bot - 0.08, ps1_bot + 0.08, ps1_bot],
        [bar_top, bar_top + al, bar_top + al, bar_top], color=c, lw=1.0)

# ===== 区域标签 =====
ax.text(1.5, 8.8, '推理前处理', fontsize=11, fontweight='bold', color='black',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=c, lw=1.0))
ax.text(1.5, 5.0, '推理与噪声注入', fontsize=11, fontweight='bold', color='black',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=c, lw=1.0))

plt.savefig('D:/grad_medical/grad_doc/charts/fig_4_4_privacy_flow_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图4-4已重新生成')
