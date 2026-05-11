"""生成图3.2 三类任务对比示意图（中文版）
根据 /root/InterMoBA_MTL 实际代码：
- 无课程学习（curriculum=off），所有任务同时训练
- 双数据源交替采样：energy 30% / affinity+pose 70%
- 五个任务头按 task_mask 自动路由
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# ── 中文字体 ──
_fp_r = fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
_fp_b = fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
def F(sz=10, bold=False):
    fp = (_fp_b if bold else _fp_r).copy(); fp.set_size(sz); return fp

fig, axes = plt.subplots(1, 3, figsize=(15, 7.8))
for ax in axes:
    ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis('off')

header_bg = {'energy': '#D4A854', 'pose': '#4A9E8E', 'affinity': '#A85C5C'}
bottom_c  = {'energy': '#B8860B', 'pose': '#2E7D6F', 'affinity': '#8B3A3A'}
table_y = [5.6, 4.85, 4.1, 3.35, 2.6, 1.85]

def draw_header(ax, title, subtitle, key):
    r = FancyBboxPatch((1, 10.8), 8, 0.9, boxstyle="round,pad=0.15",
                        facecolor=header_bg[key], edgecolor='none', alpha=0.85)
    ax.add_patch(r)
    ax.text(5, 11.25, title, ha='center', va='center', fontproperties=F(14, True), color='white')
    ax.text(5, 10.35, subtitle, ha='center', va='center', fontproperties=F(10), color='#666')

def draw_table(ax, labels, values):
    for i, (lab, val) in enumerate(zip(labels, values)):
        yp = table_y[i]
        ax.text(0.5, yp, lab, ha='left', va='center', fontproperties=F(9, True), color='#333')
        ax.text(3.2, yp, val, ha='left', va='center', fontproperties=F(8.5), color='#555')
        if i < len(labels) - 1:
            ax.plot([0.3, 9.7], [yp - 0.38, yp - 0.38], color='#ddd', lw=0.5)

ROW_LABELS = ['输出', '损失函数', '数据来源', '评估指标', '采样策略', '任务掩码']

# ═══ Column 1: 能量辅助 ═══
ax = axes[0]
draw_header(ax, '能量辅助', '原子对级', 'energy')
# atom pair
for cx, lbl in [(3.2, 'N'), (6.8, 'O')]:
    ax.add_patch(Circle((cx, 8.5), 0.55, fc='#D6EAF8', ec='#5B9BD5', lw=1.5))
    ax.text(cx, 8.5, lbl, ha='center', va='center', fontproperties=F(13, True), color='#2C5F8A')
ax.annotate('', xy=(6.2, 8.5), xytext=(3.8, 8.5),
            arrowprops=dict(arrowstyle='<->', color='#5B9BD5', lw=1.2, ls='--'))
ax.text(5, 8.95, r'$d_{ij}$', ha='center', va='center', fontsize=11, color='#5B9BD5')
# gaussian
xg = np.linspace(1.5, 8.5, 100)
ax.plot(xg, 1.2*np.exp(-0.3*(xg-5)**2)+7.0, color='#B8860B', lw=1.8)
ax.text(5, 6.45, '高斯能量项 ', ha='right', va='center', fontproperties=F(9), color='#555')
ax.text(5, 6.45, r'$E_k(d_{ij})$', ha='left', va='center', fontsize=9, color='#555')
draw_table(ax, ROW_LABELS,
    ['g_score, atom_loss', 'MDN + 原子类型 CE', 'energy 子集 (30%)',
     '能量拟合误差', '交替采样, p=0.3', 'energy batch 激活'])
ax.text(5, 0.8, '局部（原子对）', ha='center', va='center', fontproperties=F(11, True), color=bottom_c['energy'])

# ═══ Column 2: 姿态选择 ═══
ax = axes[1]
draw_header(ax, '姿态选择', '候选构象级', 'pose')
ax.add_patch(mpatches.Ellipse((5, 8.2), 6, 3.2, fc='#F0F5E8', ec='#8FBC8F', lw=1.5, alpha=0.6))
ax.text(2.5, 9.5, '口袋', ha='center', va='center', fontproperties=F(9), color='#6B8E6B')
for idx, (col, lbl) in enumerate(zip(['#2E7D32','#C0CA33','#999'], ['#1','#2','#3'])):
    xp = [3.0, 4.5, 6.0, 7.0]
    yp = [7.5+0.8*np.sin(i+idx*0.8)+(2-idx)*0.3 for i in range(4)]
    ax.plot(xp, yp, color=col, lw=1.8, marker='o', ms=4)
    ax.text(xp[-1]+0.3, yp[-1], lbl, fontsize=8, color=col, fontweight='bold')
ax.text(5, 6.2, '排序候选构象', ha='center', va='center', fontproperties=F(9), color='#555')
draw_table(ax, ROW_LABELS,
    ['Top-k 排序得分', '排序 / BCE', 'affinity+pose 子集 (70%)',
     'AUROC / Top-k', '交替采样, p=0.7', 'aff_pose batch 激活'])
ax.text(5, 0.8, '候选（构象集）', ha='center', va='center', fontproperties=F(11, True), color=bottom_c['pose'])

# ═══ Column 3: 亲和力回归 ═══
ax = axes[2]
draw_header(ax, '亲和力回归', '复合物级', 'affinity')
ax.add_patch(Circle((4.0, 8.3), 1.5, fc='#E8D5D5', ec='#A85C5C', lw=1.2, alpha=0.5))
ax.add_patch(Circle((6.0, 8.3), 1.0, fc='#F5E6D0', ec='#D4A854', lw=1.2, alpha=0.5))
ax.text(3.2, 8.3, '蛋白质', ha='center', va='center', fontproperties=F(9), color='#8B3A3A')
ax.text(6.5, 8.3, '配体', ha='center', va='center', fontproperties=F(9), color='#B8860B')
ax.annotate(r'$\hat{y}_{aff}$ = pK$_d$', xy=(9.0, 7.5), xytext=(7.2, 8.0),
            fontsize=9, color='#8B3A3A',
            arrowprops=dict(arrowstyle='->', color='#8B3A3A', lw=1.2))
draw_table(ax, ROW_LABELS,
    ['标量 y_aff', 'MSE / Huber (w=0.1)', 'affinity+pose 子集 (70%)',
     'Pearson / 逐靶点', '交替采样, p=0.7', 'aff_pose batch 激活'])
ax.text(5, 0.8, '全局（复合物）', ha='center', va='center', fontproperties=F(11, True), color=bottom_c['affinity'])

# ── Bottom arrow ──
fig.text(0.5, 0.03, '监督粒度', ha='center', va='center', fontproperties=F(11), color='#555')
ax_arrow = fig.add_axes([0.12, 0.045, 0.78, 0.01])
ax_arrow.axis('off')
ax_arrow.annotate('', xy=(1, 0.5), xytext=(0, 0.5),
                  arrowprops=dict(arrowstyle='->', color='#888', lw=1.5))

plt.subplots_adjust(left=0.03, right=0.97, top=0.95, bottom=0.08, wspace=0.15)
plt.savefig('/root/thesis_final/images/task_comparison.png', dpi=200, bbox_inches='tight', facecolor='white')
print('DONE -> /root/thesis_final/images/task_comparison.png')
