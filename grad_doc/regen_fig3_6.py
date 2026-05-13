#!/usr/bin/env python3
"""重新生成图3-6 系统ER图 - 业界标准实体关系图格式，黑白配色"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

c = '#222222'

# Entity definitions with center positions
entities_data = [
    {'name': '用户',       'attrs': ['用户ID (PK)', '用户名', '密码', '角色'],                   'cx': 4.0,  'cy': 10.5},
    {'name': '隐私配置',   'attrs': ['配置ID (PK)', '用户ID (FK)', 'ε参数', 'δ参数', '预算额度'], 'cx': 14.0, 'cy': 10.5},
    {'name': '患者',       'attrs': ['患者ID (PK)', '用户ID (FK)', '姓名', '年龄', '性别'],       'cx': 1.5,  'cy': 7.0},
    {'name': '推荐记录',   'attrs': ['记录ID (PK)', '患者ID (FK)', '用户ID (FK)', '推荐结果', '创建时间'], 'cx': 7.0, 'cy': 7.0},
    {'name': '药品',       'attrs': ['药品ID (PK)', '药品名', '适应症', '禁忌症'],               'cx': 13.0, 'cy': 7.0},
    {'name': '健康档案',   'attrs': ['档案ID (PK)', '患者ID (FK)', '慢性病', '过敏史'],          'cx': 1.5,  'cy': 3.5},
    {'name': '隐私记录',   'attrs': ['记录ID (PK)', '用户ID (FK)', '消耗ε', '事件类型', '时间戳'], 'cx': 14.0, 'cy': 3.5},
]

box_w = 2.8
attr_h = 0.35
header_h = 0.45
sep_gap = 0.10
pad_top = 0.12
pad_bot = 0.12

# Calculate box dimensions and edge positions
for e in entities_data:
    n = len(e['attrs'])
    e['box_h'] = pad_top + header_h + sep_gap + n * attr_h + pad_bot
    e['top'] = e['cy'] + e['box_h'] / 2
    e['bot'] = e['cy'] - e['box_h'] / 2
    e['left'] = e['cx'] - box_w / 2
    e['right'] = e['cx'] + box_w / 2

ent_map = {e['name']: e for e in entities_data}

# Verification
print("坐标验证:")
for e in entities_data:
    print(f"  {e['name']}: bot={e['bot']:.2f} top={e['top']:.2f} left={e['left']:.2f} right={e['right']:.2f}")

fig, ax = plt.subplots(figsize=(18, 13))
ax.set_xlim(-1, 17)
ax.set_ylim(1, 13)
ax.axis('off')

# ===== Draw entity boxes =====
for e in entities_data:
    lx, rx = e['left'], e['right']
    ty, by = e['top'], e['bot']

    # Box border
    ax.plot([lx, rx, rx, lx, lx], [by, by, ty, ty, by], color=c, lw=1.5)

    # Header: entity name
    header_bot = ty - pad_top - header_h
    ax.text(e['cx'], (ty - pad_top + header_bot) / 2, e['name'],
            ha='center', va='center', fontsize=14, fontweight='bold', color='black')

    # Separator line
    ax.plot([lx + 0.05, rx - 0.05], [header_bot, header_bot], color=c, lw=1.0)

    # Attributes
    attr_y_start = header_bot - sep_gap
    for j, attr in enumerate(e['attrs']):
        ay = attr_y_start - j * attr_h
        is_pk = '(PK)' in attr
        is_fk = '(FK)' in attr
        if is_pk:
            ax.text(lx + 0.15, ay, attr, ha='left', va='center', fontsize=11,
                    color='black', fontweight='bold')
        elif is_fk:
            ax.text(lx + 0.15, ay, attr, ha='left', va='center', fontsize=11,
                    color='#444444')
        else:
            ax.text(lx + 0.15, ay, attr, ha='left', va='center', fontsize=11,
                    color='black')

# ===== Relationship lines with cardinality =====
# Each connection: specify from/to edges and cardinality
connections = [
    # (from_name, from_edge, to_name, to_edge, from_card, to_card, label, label_offset)
    # edge: 'bot', 'top', 'left', 'right'
    ('用户',       'bot',  '患者',     'top',  '1', 'N', '管理',  (0.5, 0.3)),
    ('用户',       'bot',  '推荐记录', 'top',  '1', 'N', '生成',  (-0.5, 0.3)),
    ('用户',       'right','隐私配置', 'left', '1', '1', '配置',  (0, 0.3)),
    ('患者',       'bot',  '健康档案', 'top',  '1', '1', '拥有',  (0.5, 0)),
    ('患者',       'right','推荐记录', 'left', '1', 'N', '获得',  (0, 0.3)),
    ('药品',       'left', '推荐记录', 'right','N', 'M', '包含',  (0, 0.3)),
    ('隐私配置',   'bot',  '隐私记录', 'top',  '1', 'N', '记录',  (0.5, 0)),
]

for from_name, from_edge, to_name, to_edge, fc, tc, label, lbl_off in connections:
    fe = ent_map[from_name]
    te = ent_map[to_name]

    # Calculate connection point on entity edge
    def get_edge_point(entity, edge):
        if edge == 'bot':  return (entity['cx'], entity['bot'])
        if edge == 'top':  return (entity['cx'], entity['top'])
        if edge == 'left': return (entity['left'], entity['cy'])
        if edge == 'right':return (entity['right'], entity['cy'])

    fx, fy = get_edge_point(fe, from_edge)
    tx, ty = get_edge_point(te, to_edge)

    # Draw connection line
    ax.plot([fx, tx], [fy, ty], color=c, lw=1.3)

    # Cardinality labels near endpoints
    # Offset from endpoint toward outside of entity
    dx = tx - fx
    dy = ty - fy

    # From cardinality: offset away from line direction, toward entity outside
    if from_edge == 'bot':
        fc_x, fc_y = fx + 0.35, fy - 0.20
    elif from_edge == 'top':
        fc_x, fc_y = fx + 0.35, fy + 0.20
    elif from_edge == 'left':
        fc_x, fc_y = fx - 0.30, fy + 0.25
    elif from_edge == 'right':
        fc_x, fc_y = fx + 0.30, fy + 0.25

    ax.text(fc_x, fc_y, fc, fontsize=11, color='black',
            ha='center', va='center', fontweight='bold')

    # To cardinality: offset away from line direction, toward entity outside
    if to_edge == 'bot':
        tc_x, tc_y = tx + 0.35, ty - 0.20
    elif to_edge == 'top':
        tc_x, tc_y = tx + 0.35, ty + 0.20
    elif to_edge == 'left':
        tc_x, tc_y = tx - 0.30, ty + 0.25
    elif to_edge == 'right':
        tc_x, tc_y = tx + 0.30, ty + 0.25

    ax.text(tc_x, tc_y, tc, fontsize=11, color='black',
            ha='center', va='center', fontweight='bold')

    # Relationship label at midpoint with offset
    mid_x = (fx + tx) / 2 + lbl_off[0]
    mid_y = (fy + ty) / 2 + lbl_off[1]
    ax.text(mid_x, mid_y, label, fontsize=10, color='black',
            ha='center', va='center')

plt.savefig('D:/grad_medical/grad_doc/charts/fig_3_6_er_diagram_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图3-6已重新生成')