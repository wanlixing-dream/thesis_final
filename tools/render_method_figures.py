"""Render method figures following Nature / Wong (Okabe-Ito) style guidelines.

Palette: Okabe-Ito (Wong, Nature Methods 2011) for colorblind-safe categorical data.
Fonts: Helvetica/Arial-like sans-serif for Latin, STZhongsong for CJK fallback.
Style: Axes with tick marks, no background gridlines, black text, no drop shadows.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
FONT_PATH = ROOT / "STZhongsong.ttf"

# Okabe-Ito / Wong palette (Nature Methods, 2011) - colorblind safe.
WONG = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
}

# Neutral light tints for non-data module fills.
TINT = {
    "input": "#E7F1F7",     # from sky blue
    "data": "#E3EEF7",      # from blue
    "encoder": "#E8F2ED",   # from bluish green
    "heads": "#FBF0DE",     # from orange
    "strategy": "#F8E5D6",  # from vermillion
    "accent": "#F3E1EC",    # from reddish purple
    "phase_a": "#F2F5F8",
    "phase_b": "#E9EEF3",
}

INK = "#000000"
AXIS = "#333333"
MUTED = "#444444"

font_manager.fontManager.addfont(str(FONT_PATH))
CJK_FONT = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", CJK_FONT, "DejaVu Sans"],
    "axes.unicode_minus": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def add_box(ax, x, y, w, h, text, *, fc, ec=INK, lw=1.0, fontsize=10.5, linespacing=1.35, fontweight="normal"):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.018",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=INK,
        linespacing=linespacing,
        fontweight=fontweight,
    )
    return patch


def add_arrow(ax, x1, y1, x2, y2, *, color=INK, lw=1.1, style="-|>"):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=style,
            color=color,
            linewidth=lw,
            shrinkA=0,
            shrinkB=0,
            mutation_scale=9,
        ),
    )


def draw_system_architecture(output_path: Path):
    # ── SCI style: 3-tier font ladder ──
    #   title  = 13 pt bold
    #   body   = 10 pt  (all boxes, layer labels)
    #   note   = 8.5 pt (annotations, legend)
    FS_TITLE, FS_BODY, FS_NOTE = 13, 10, 8.5

    fig, ax = plt.subplots(figsize=(12.5, 8.8), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Title
    ax.text(0.06, 0.96, "InterMoBA-MTL 方法总体架构",
            fontsize=FS_TITLE, fontweight="bold", color=INK)
    ax.text(0.06, 0.935, "双数据源、多任务共享表示与训练策略协同的系统化组织",
            fontsize=FS_NOTE, color=MUTED)

    # ── 5 layers, evenly spaced (centre gap = 0.17) ──
    #   Layer centres: 0.82, 0.65, 0.48, 0.31, 0.14
    #   Box height = 0.10 for every layer (encoder 0.11)
    LY = [0.82, 0.65, 0.48, 0.31, 0.14]   # layer centres
    BH = 0.10                                # default box height

    # Layer labels (left column, bold, FS_BODY)
    layer_names = ["输入数据层", "多任务数据组织层", "共享编码层",
                   "任务输出层", "训练策略层"]
    for i, name in enumerate(layer_names):
        ax.text(0.05, LY[i] + BH / 2 + 0.015, name,
                fontsize=FS_BODY, color=INK, fontweight="bold")

    # ── Layer 1: Input data ──
    add_box(ax, 0.19, LY[0] - BH / 2, 0.24, BH, "能量数据源",
            fc=TINT["input"], ec=WONG["sky_blue"], lw=1.2, fontsize=FS_BODY)
    add_box(ax, 0.57, LY[0] - BH / 2, 0.24, BH, "亲和力-姿态数据源",
            fc=TINT["input"], ec=WONG["sky_blue"], lw=1.2, fontsize=FS_BODY)

    # ── Layer 2: Data organisation ──
    add_box(
        ax, 0.27, LY[1] - BH / 2, 0.46, BH,
        "多任务数据模块\n交替批次采样  ·  task_id  ·  task_mask",
        fc=TINT["data"], ec=WONG["blue"], lw=1.2,
        fontsize=FS_BODY, fontweight="bold",
    )

    # ── Layer 3: Shared encoder ──
    enc_h = 0.11
    add_box(
        ax, 0.20, LY[2] - enc_h / 2, 0.60, enc_h,
        "共享图表示编码器\n复合图特征提取  ·  上下文交互建模",
        fc=TINT["encoder"], ec=WONG["bluish_green"], lw=1.2,
        fontsize=FS_BODY, fontweight="bold",
    )
    add_box(ax, 0.665, LY[2] + 0.01, 0.12, 0.05,
            "MoBA 稀疏增强",
            fc="white", ec=WONG["bluish_green"], lw=0.9, fontsize=FS_NOTE)

    # ── Layer 4: Task heads ──
    head_w = 0.20
    head_y = LY[3] - BH / 2
    add_box(ax, 0.15, head_y, head_w, BH, "亲和力回归头",
            fc=TINT["heads"], ec=WONG["orange"], lw=1.2, fontsize=FS_BODY)
    add_box(ax, 0.40, head_y, head_w, BH, "姿态选择头",
            fc=TINT["heads"], ec=WONG["orange"], lw=1.2, fontsize=FS_BODY)
    add_box(ax, 0.65, head_y, head_w, BH,
            "能量相关输出头\ng_score · g_score_pos",
            fc=TINT["heads"], ec=WONG["orange"], lw=1.2, fontsize=FS_BODY)

    # ── Layer 5: Training strategy ──
    strat_h = 0.08
    strat_y = LY[4] - strat_h / 2
    add_box(ax, 0.13, strat_y, 0.17, strat_h, "多任务损失加权",
            fc=TINT["strategy"], ec=WONG["vermillion"], lw=1.2, fontsize=FS_BODY)
    add_box(ax, 0.33, strat_y, 0.14, strat_h, "课程学习",
            fc=TINT["strategy"], ec=WONG["vermillion"], lw=1.2, fontsize=FS_BODY)
    add_box(ax, 0.50, strat_y, 0.14, strat_h, "PCGrad",
            fc=TINT["strategy"], ec=WONG["vermillion"], lw=1.2, fontsize=FS_BODY)
    add_box(ax, 0.67, strat_y, 0.18, strat_h, "任务路由",
            fc=TINT["strategy"], ec=WONG["vermillion"], lw=1.2, fontsize=FS_BODY)

    # ── Arrows: data flow (top-down, black) ──
    add_arrow(ax, 0.31, LY[0] - BH / 2, 0.43, LY[1] + BH / 2)
    add_arrow(ax, 0.69, LY[0] - BH / 2, 0.57, LY[1] + BH / 2)
    add_arrow(ax, 0.50, LY[1] - BH / 2, 0.50, LY[2] + enc_h / 2)
    add_arrow(ax, 0.40, LY[2] - enc_h / 2, 0.25, LY[3] + BH / 2)
    add_arrow(ax, 0.50, LY[2] - enc_h / 2, 0.50, LY[3] + BH / 2)
    add_arrow(ax, 0.60, LY[2] - enc_h / 2, 0.75, LY[3] + BH / 2)

    # ── Arrows: strategy feedback (vermillion, upward) ──
    add_arrow(ax, 0.21, strat_y + strat_h, 0.25, head_y,
              color=WONG["vermillion"], lw=1.0, style="-|>")
    add_arrow(ax, 0.40, strat_y + strat_h, 0.50, head_y,
              color=WONG["vermillion"], lw=1.0, style="-|>")
    add_arrow(ax, 0.57, strat_y + strat_h, 0.55, LY[2] - enc_h / 2,
              color=WONG["vermillion"], lw=1.0, style="-|>")
    add_arrow(ax, 0.76, strat_y + strat_h, 0.70, LY[2] - enc_h / 2,
              color=WONG["vermillion"], lw=1.0, style="-|>")

    # ── Right-side annotations ──
    ax.text(0.86, 0.65, "同一训练框架中\n组织异构监督信号",
            fontsize=FS_NOTE, color=INK, ha="left", va="center", linespacing=1.35)
    ax.text(0.86, 0.48, "共享表示服务于\n不同任务输出",
            fontsize=FS_NOTE, color=INK, ha="left", va="center", linespacing=1.35)

    # ── Arrow legend (top-right) ──
    lx, ly = 0.855, 0.880
    lw_l, lh_l = 0.135, 0.075
    ax.add_patch(FancyBboxPatch(
        (lx, ly), lw_l, lh_l,
        boxstyle="round,pad=0.006,rounding_size=0.010",
        linewidth=0.7, edgecolor=AXIS, facecolor="white",
    ))
    ax.text(lx + 0.006, ly + lh_l - 0.012, "箭头图例",
            fontsize=FS_NOTE, color=INK, fontweight="bold", ha="left", va="center")
    add_arrow(ax, lx + 0.008, ly + 0.032, lx + 0.035, ly + 0.032,
              color=INK, lw=1.1)
    ax.text(lx + 0.040, ly + 0.032, "数据流向",
            fontsize=FS_NOTE, color=INK, ha="left", va="center")
    add_arrow(ax, lx + 0.008, ly + 0.012, lx + 0.035, ly + 0.012,
              color=WONG["vermillion"], lw=1.1)
    ax.text(lx + 0.040, ly + 0.012, "策略反馈",
            fontsize=FS_NOTE, color=INK, ha="left", va="center")

    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)


def linear_ramp(x, start, end):
    y = (x - start) / max(end - start, 1e-8)
    return y.clip(0.0, 1.0)


def gaussian_curve(x, mu, sigma, amplitude):
    return amplitude * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def build_component_maps():
    ligand = np.arange(15)[:, None]
    pocket = np.arange(30)[None, :]

    vdw_like_1 = (
        0.85 * np.exp(-((pocket - 7.0) ** 2) / 42.0 - ((ligand - 4.0) ** 2) / 18.0)
        + 0.55 * np.exp(-((pocket - 21.0) ** 2) / 60.0 - ((ligand - 10.0) ** 2) / 28.0)
    )
    vdw_like_2 = (
        0.70 * np.exp(-((pocket - 12.0) ** 2) / 50.0 - ((ligand - 6.0) ** 2) / 18.0)
        + 0.48 * np.exp(-((pocket - 25.0) ** 2) / 18.0 - ((ligand - 12.0) ** 2) / 10.0)
    )

    hydro_gate = (((pocket >= 4) & (pocket <= 11)) | ((pocket >= 18) & (pocket <= 27))).astype(float)
    ligand_hydro = (((ligand >= 2) & (ligand <= 5)) | ((ligand >= 8) & (ligand <= 11))).astype(float)
    hydro = (
        0.80 * np.exp(-((pocket - 9.0) ** 2) / 32.0 - ((ligand - 4.0) ** 2) / 10.0)
        + 0.68 * np.exp(-((pocket - 23.0) ** 2) / 24.0 - ((ligand - 9.0) ** 2) / 12.0)
    ) * hydro_gate * ligand_hydro

    hbond = np.zeros_like(vdw_like_1)
    for pocket_center, ligand_center, amplitude in [
        (8.0, 5.0, 1.00),
        (10.0, 6.0, 0.88),
        (12.0, 7.0, 0.72),
        (22.0, 10.0, 0.82),
        (24.0, 12.0, 0.66),
    ]:
        hbond += amplitude * np.exp(-((pocket - pocket_center) ** 2) / 1.6 - ((ligand - ligand_center) ** 2) / 1.3)

    components = [vdw_like_1, vdw_like_2, hydro, hbond]
    return [component / max(component.max(), 1e-8) for component in components]


def draw_gaussian_components(output_path: Path):
    x = np.linspace(-1.5, 5.5, 700)
    curves = [
        (gaussian_curve(x, 0.55, 0.42, 0.92), WONG["blue"], "类 vdW 分量 1（全对开放）"),
        (gaussian_curve(x, 1.65, 0.62, 0.78), WONG["sky_blue"], "类 vdW 分量 2（全对开放）"),
        (gaussian_curve(x, 2.05, 0.52, 0.74), WONG["bluish_green"], "疏水分量（疏水门控）"),
        (gaussian_curve(x, 2.78, 0.30, 0.60), WONG["reddish_purple"], "氢键分量（供受体门控）"),
    ]

    fig, ax = plt.subplots(figsize=(7.4, 4.4), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for y, color, label in curves:
        ax.plot(x, y, color=color, linewidth=2.2, label=label)

    ax.axvline(2.0, color=AXIS, linewidth=1.0, linestyle=(0, (2, 3)), label="碰撞阈值 = 2.0 Å")

    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(0.0, 1.02)
    ax.set_xlabel("表面距离 d (Å)", fontsize=11, color=INK)
    ax.set_ylabel("相对分量响应", fontsize=11, color=INK)
    ax.set_title("四分量 MDN 距离头", fontsize=13.5, pad=10, color=INK, fontweight="bold")

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.9)

    ax.tick_params(axis="both", which="major", direction="out", length=3.5, width=0.9, colors=AXIS, labelsize=9.5)
    ax.grid(False)
    leg = ax.legend(frameon=False, loc="upper right", fontsize=9.2, handlelength=2.3)
    for text in leg.get_texts():
        text.set_color(INK)

    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)


def draw_energy_decomposition(output_path: Path):
    component_maps = build_component_maps()
    titles = ["类 vdW 分量 1", "类 vdW 分量 2", "疏水门控分量", "氢键门控分量"]
    colors = ["Blues", "PuBu", "Greens", "Purples"]

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 8.5), dpi=300)
    fig.patch.set_facecolor("white")
    fig.suptitle("原子对分量响应图", fontsize=13.5, color=INK, fontweight="bold", y=0.98)

    for ax, component, title, cmap in zip(axes.flatten(), component_maps, titles, colors):
        im = ax.imshow(component, cmap=cmap, aspect="auto", origin="upper", vmin=0.0, vmax=1.0)
        ax.set_title(title, fontsize=11, color=INK)
        ax.set_xlabel("口袋原子索引", fontsize=9.5, color=INK)
        ax.set_ylabel("配体原子索引", fontsize=9.5, color=INK)
        ax.tick_params(axis="both", which="major", direction="out", length=2.8, width=0.8, colors=AXIS, labelsize=8.5)
        for side in ("top", "right", "left", "bottom"):
            ax.spines[side].set_color(AXIS)
            ax.spines[side].set_linewidth(0.8)
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=8.5, colors=AXIS)
        cbar.outline.set_edgecolor(AXIS)
        cbar.outline.set_linewidth(0.7)
        cbar.set_label("相对响应", fontsize=8.8, color=INK)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(output_path, bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)


def draw_atom_contributions(output_path: Path):
    vdw_like_1, vdw_like_2, hydro, hbond = build_component_maps()
    per_atom = [component.sum(axis=1) for component in (vdw_like_1, vdw_like_2, hydro, hbond)]
    per_atom = [values / max(values.max(), 1e-8) for values in per_atom]
    x = np.arange(per_atom[0].shape[0])
    width = 0.20

    fig, ax = plt.subplots(figsize=(9.2, 4.5), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.bar(x - 1.5 * width, per_atom[0], width=width, color=WONG["blue"], label="vdW-like 1")
    ax.bar(x - 0.5 * width, per_atom[1], width=width, color=WONG["sky_blue"], label="vdW-like 2")
    ax.bar(x + 0.5 * width, per_atom[2], width=width, color=WONG["bluish_green"], label="Hydrophobic")
    ax.bar(x + 1.5 * width, per_atom[3], width=width, color=WONG["reddish_purple"], label="H-bond")

    ax.set_xlabel("Ligand atom index", fontsize=11, color=INK)
    ax.set_ylabel("Relative aggregated contribution", fontsize=11, color=INK)
    ax.set_title("Per-atom local contribution summary", fontsize=13.5, pad=10, color=INK, fontweight="bold")
    ax.set_xticks(x)
    ax.set_ylim(0.0, 1.08)

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.9)

    ax.tick_params(axis="both", which="major", direction="out", length=3.5, width=0.9, colors=AXIS, labelsize=9.5)
    ax.grid(False)
    leg = ax.legend(frameon=False, loc="upper right", fontsize=9.3)
    for text in leg.get_texts():
        text.set_color(INK)

    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)


def draw_weight_scheduler(output_path: Path):
    x = np.linspace(0, 1, 500)
    energy = np.ones_like(x)
    pose = linear_ramp(x, 0.15, 0.35)
    affinity = linear_ramp(x, 0.35, 0.60)

    fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Phase background bands - alternating neutral tints, low-saturation.
    ax.axvspan(0.00, 0.15, color=TINT["phase_a"], zorder=0)
    ax.axvspan(0.15, 0.35, color=TINT["phase_b"], zorder=0)
    ax.axvspan(0.35, 0.60, color=TINT["phase_a"], zorder=0)
    ax.axvspan(0.60, 1.00, color=TINT["phase_b"], zorder=0)

    # Phase dividers - thin dark vertical lines.
    for xv in (0.15, 0.35, 0.60):
        ax.axvline(xv, color=AXIS, linewidth=0.6, linestyle=(0, (4, 3)), alpha=0.7, zorder=1)

    # Data curves - Wong colors, distinct linestyles for grayscale legibility.
    ax.plot(x, energy, color=WONG["blue"], linewidth=2.0,
            label="能量任务", zorder=3)
    ax.plot(x, pose, color=WONG["vermillion"], linewidth=2.0,
            linestyle="--", label="姿态任务", zorder=3)
    ax.plot(x, affinity, color=WONG["bluish_green"], linewidth=2.0,
            linestyle=":", label="亲和力任务", zorder=3)

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.08, 1.08)
    ax.set_xlabel("训练进度 (归一化)", fontsize=11, color=INK, labelpad=22)
    ax.set_ylabel("任务激活系数", fontsize=11, color=INK)
    ax.set_title("三阶段课程学习中的任务调度示意",
                 fontsize=13.5, pad=12, color=INK, fontweight="bold")

    # Phase labels - placed inside top of plot area, above data lines.
    ax.text(0.075, 0.04, "第一阶段", transform=ax.transData,
            ha="center", va="center", fontsize=9.5, color=INK)
    ax.text(0.25, 0.04, "第二阶段", transform=ax.transData,
            ha="center", va="center", fontsize=9.5, color=INK)
    ax.text(0.475, 0.04, "第三阶段", transform=ax.transData,
            ha="center", va="center", fontsize=9.5, color=INK)
    ax.text(0.80, 0.04, "全任务协同", transform=ax.transData,
            ha="center", va="center", fontsize=9.5, color=INK)

    # Axes styling - visible ticks, no gridlines (Nature spec).
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.9)

    ax.tick_params(axis="both", which="major",
                   direction="out", length=3.5, width=0.9,
                   colors=AXIS, labelsize=9.5)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylim(-0.02, 1.08)

    # No gridlines per Nature guidelines.
    ax.grid(False)

    # Legend - no frame, black text (colour conveyed by line segments).
    leg = ax.legend(frameon=False, loc="center right",
                    fontsize=10, labelcolor=INK, handlelength=2.6)
    for text in leg.get_texts():
        text.set_color(INK)

    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)


def draw_preprocess_pipeline(output_path: Path):
    fig, ax = plt.subplots(figsize=(13.0, 7.0), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.text(0.04, 0.95, "Protein-ligand preprocessing workflow (code-aligned)",
            fontsize=16.0, fontweight="bold", color=INK)
    ax.text(0.04, 0.915,
            "CSV index -> structure loading -> complex merge -> graph conversion -> quality filtering -> LMDB/CSV cache",
            fontsize=10.8, color=MUTED)

    # Top row: data construction path.
    add_box(
        ax, 0.05, 0.66, 0.18, 0.17,
        "1) CSV读取与样本过滤\n_filter_df\n(阈值/类型筛选)",
        fc=TINT["input"], ec=WONG["sky_blue"], lw=1.2, fontsize=10.8,
    )
    add_box(
        ax, 0.27, 0.66, 0.19, 0.17,
        "2) 口袋与配体加载\n_read_pocket + sdf_load\n并行读取(pmap)",
        fc=TINT["input"], ec=WONG["sky_blue"], lw=1.2, fontsize=10.8,
    )
    add_box(
        ax, 0.50, 0.66, 0.19, 0.17,
        "3) 复合物构建\nmerge_sdf_pdb_by_rdkit\nPLIP风格相互作用关系",
        fc=TINT["data"], ec=WONG["blue"], lw=1.2, fontsize=10.8,
    )
    add_box(
        ax, 0.73, 0.66, 0.20, 0.17,
        "4) 图样本转换\ncomplex_to_data\npmap_chunked并行",
        fc=TINT["encoder"], ec=WONG["bluish_green"], lw=1.2, fontsize=10.8,
    )

    # Bottom row: quality control and persistence.
    add_box(
        ax, 0.10, 0.33, 0.22, 0.17,
        "5) 有效样本过滤\nNone样本剔除 + 标签回填\n_assign_label2x",
        fc=TINT["heads"], ec=WONG["orange"], lw=1.2, fontsize=10.8,
    )
    add_box(
        ax, 0.39, 0.33, 0.23, 0.17,
        "6) 缓存落盘\nLmdbPPI.make_shared\n同时写 cache.csv",
        fc=TINT["strategy"], ec=WONG["vermillion"], lw=1.2, fontsize=10.8,
    )
    add_box(
        ax, 0.68, 0.33, 0.25, 0.17,
        "7) 数据集构造与划分\n_get_dataset + split\nTrain / Val / Test",
        fc=TINT["accent"], ec=WONG["reddish_purple"], lw=1.2, fontsize=10.8,
    )

    # Arrows (main flow).
    add_arrow(ax, 0.23, 0.745, 0.27, 0.745)
    add_arrow(ax, 0.46, 0.745, 0.50, 0.745)
    add_arrow(ax, 0.69, 0.745, 0.73, 0.745)
    add_arrow(ax, 0.83, 0.66, 0.20, 0.50)
    add_arrow(ax, 0.32, 0.415, 0.39, 0.415)
    add_arrow(ax, 0.62, 0.415, 0.68, 0.415)

    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", facecolor="white", dpi=300)
    plt.close(fig)


def main():
    IMAGES.mkdir(parents=True, exist_ok=True)
    draw_system_architecture(IMAGES / "system_architecture.png")
    draw_weight_scheduler(IMAGES / "weight_scheduler.png")
    draw_gaussian_components(IMAGES / "gaussian_components.png")
    draw_energy_decomposition(IMAGES / "energy_decomposition.png")
    draw_atom_contributions(IMAGES / "atom_contributions.png")
    draw_preprocess_pipeline(IMAGES / "preprocess_pipeline.png")


if __name__ == "__main__":
    main()
