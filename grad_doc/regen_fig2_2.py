#!/usr/bin/env python3
"""重新生成图2-2 JWT认证流程 - 自动计算无重叠坐标"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

bw = 3.5   # 框宽
bh = 1.0   # 框高
cx = 4.0   # 主列中心x
rx = 8.0   # 右分支中心x
dw = 1.8   # 菱形半宽
dh = 0.8   # 菱形半高
c = '#222222'
sp = 0.35  # 相邻元素间距

# 从顶部开始自动计算所有y坐标
# 定义元素类型: 'box' 或 'diamond'
elements = [
    ('box',   '用户登录请求\n(提交用户名/密码)'),
    ('box',   '后端接收请求\nSpring Security验证'),
    ('diamond','验证成功'),
    ('box',   '生成JWT令牌\n(HMAC-SHA256签名)'),
    ('box',   '返回JWT令牌给前端\n(localStorage存储)'),
    ('box',   '前端携带JWT请求\n(Authorization Header)'),
    ('box',   '后端解析验证JWT\n(签名+过期检查)'),
    ('diamond','令牌有效'),
    ('box',   '返回请求资源\n(业务数据)'),
]

# 计算每个元素的 [top_edge, bottom_edge, center_y]
positions = []
y_top = 16.5  # 起始顶部

for etype, text in elements:
    if etype == 'box':
        bot = y_top - bh
        positions.append((y_top, bot, y_top - bh/2, text, etype))
        next_top = bot - sp
    else:  # diamond
        bot = y_top - 2*dh
        center = y_top - dh
        positions.append((y_top, bot, center, text, etype))
        next_top = bot - sp
    y_top = next_top

# 验证无重叠
print("坐标验证:")
for i, (top, bot, center, text, etype) in enumerate(positions):
    print(f"  {etype} [{bot:.2f}, {top:.2f}] center={center:.2f} \"{text[:15]}\"")
    if i > 0:
        # 重叠 = 上一个bottom - 当前top, 正值=有间距, 负值=重叠
        gap = positions[i-1][1] - top  # 上一个bottom - 当前top
        status = f"间距{gap:.2f}" if gap >= 0 else f"OVERLAP({gap:.2f})"
        print(f"    {status}")

# 计算画布高度
min_y = positions[-1][1] - 0.5
canvas_h = positions[0][0] + 0.5 - min_y

fig, ax = plt.subplots(figsize=(10, max(canvas_h, 8)))
ax.set_xlim(0, 10)
ax.set_ylim(min_y, positions[0][0] + 0.5)
ax.axis('off')

def draw_rect(cx, y_top, y_bot, text):
    xl = cx - bw/2
    ax.plot([xl, xl+bw, xl+bw, xl, xl], [y_bot, y_bot, y_top, y_top, y_bot], color=c, lw=1.5)
    ax.text(cx, (y_top+y_bot)/2, text, ha='center', va='center', fontsize=9, color='black', linespacing=1.3)

def draw_diamond(cx, y_center, text):
    top=y_center+dh; right=cx+dw; bot=y_center-dh; left=cx-dw
    xs=[cx,right,cx,left,cx]; ys=[top,y_center,bot,y_center,top]
    ax.plot(xs, ys, color=c, lw=1.5)
    ax.fill(xs, ys, color='#F5F5F5')
    ax.text(cx, y_center, text, ha='center', va='center', fontsize=9, fontweight='bold', color='black')

def arrow_v(x, y_from, y_to):
    ax.plot([x,x],[y_from,y_to], color=c, lw=1.3)
    al=0.1
    ax.plot([x,x-0.1,x+0.1,x],[y_to,y_to+al,y_to+al,y_to], color=c, lw=1.3)

def arrow_h(y, x_from, x_to):
    ax.plot([x_from,x_to],[y,y], color=c, lw=1.3)
    al=0.1
    ax.plot([x_to,x_to-al,x_to-al,x_to],[y,y+0.07,y-0.07,y], color=c, lw=1.3)

# 绘制所有主流程元素
for top, bot, center, text, etype in positions:
    if etype == 'box':
        draw_rect(cx, top, bot, text)
    else:
        draw_diamond(cx, center, text)

# 绘制右分支框 (与对应菱形同行，稍上偏移)
diamond1_yc = positions[2][2]  # 菱形1中心y
diamond2_yc = positions[7][2]  # 菱形2中心y
draw_rect(rx, diamond1_yc + bh/2, diamond1_yc - bh/2, '返回401\nUnauthorized')
draw_rect(rx, diamond2_yc + bh/2, diamond2_yc - bh/2, '返回401\n令牌无效/过期')

# 绘制纵向箭头 (从上一个元素底边到下一个元素顶边)
for i in range(len(positions)-1):
    prev_bot = positions[i][1]  # 上一个底边
    next_top = positions[i+1][0]  # 下一个顶边
    arrow_v(cx, prev_bot, next_top)

# 是/否标注
# 菱形1下方标注"是"
ax.text(cx-0.4, positions[2][1]-0.15, '是', fontsize=8, color='black', ha='center')
# 菱形2下方标注"是"
ax.text(cx-0.4, positions[7][1]-0.15, '是', fontsize=8, color='black', ha='center')

# 横向箭头 - "否"字放在菱形和右框之间
mid_x = (cx+dw + rx-bw/2) / 2
arrow_h(diamond1_yc, cx+dw, rx-bw/2)
ax.text(mid_x, diamond1_yc+0.15, '否', fontsize=8, color='black', ha='center')
arrow_h(diamond2_yc, cx+dw, rx-bw/2)
ax.text(mid_x, diamond2_yc+0.15, '否', fontsize=8, color='black', ha='center')

plt.savefig('D:/grad_medical/grad_doc/charts/fig_2_2_jwt_auth_flow_v2.png',
            dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.3)
print('✅ 图2-2已重新生成, 无重叠')