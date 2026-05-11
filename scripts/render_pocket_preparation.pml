# ============================================================
# PyMOL script: 蛋白口袋准备流程示意图 (PDB: 3w2o)
# 用法: pymol -cq render_pocket_preparation.pml
# 输出: ../images/pocket_preparation_3w2o.png
# ============================================================

# ---------- 0. 全局设置 ----------
bg_color white
set ray_opaque_background, 1
set ray_trace_mode, 1
set ray_shadows, 0
set antialias, 2
set orthoscopic, on
set depth_cue, 0
set label_size, 14
set label_color, black
set label_font_id, 7
set label_outline_color, white
set stick_radius, 0.15
set cartoon_transparency, 0.75
set surface_transparency, 0.55

# ---------- 1. 加载结构 ----------
# 从 PDB 在线获取；如果本地有文件，可替换为: load /path/to/3w2o.pdb, full_protein
fetch 3w2o, full_protein, async=0
remove solvent
remove resn HOH

# ---------- 2. 定义配体和蛋白 ----------
# 3w2o 的共晶配体残基名为 0LI
select ligand, full_protein and resn 0LI
select protein_only, full_protein and polymer.protein

# ---------- 3. 定义 Stage-1 pocket: 7 Å cutoff + 完整残基扩展 ----------
# 先选 7A 内原子，再扩展到完整残基 (byres)
select pocket_7A_atoms, protein_only within 7.0 of ligand
select pocket_7A, byres pocket_7A_atoms

# ---------- 4. 定义 Stage-2 graph neighborhood: 10 Å cutoff ----------
select graph_10A_atoms, protein_only within 10.0 of ligand
select graph_10A, byres graph_10A_atoms

# ---------- 5. 外围蛋白 (仅在 10A 之外) ----------
select outer_protein, protein_only and not graph_10A

# ============================================================
# 左图: Stage-1 Pocket Extraction (7 Å)
# ============================================================
create panel_left, full_protein
hide everything, panel_left

# 全蛋白 cartoon (浅灰, 高透明)
select left_protein, panel_left and polymer.protein
show cartoon, left_protein
color gray80, left_protein
set cartoon_transparency, 0.80, panel_left

# 配体 (黄色 sticks)
select left_ligand, panel_left and resn 0LI
show sticks, left_ligand
color yellow, left_ligand
set stick_radius, 0.20, left_ligand

# 7A pocket 残基 (cyan sticks)
select left_pocket, panel_left and polymer.protein within 7.0 of (panel_left and resn 0LI)
select left_pocket, byres left_pocket
show sticks, left_pocket
color cyan, left_pocket

# 标注关键残基
select left_label_res, left_pocket and name CA
label left_label_res, "%s%s" % (resn, resi)

# 7A 距离标尺 (从配体质心方向画一条虚线)
# 用 pseudoatom 标注
pseudoatom pk_lig_center, panel_left and resn 0LI
pseudoatom pk_7A_label, pos=[0,0,0]
# 移到配体附近手动标注
hide everything, pk_lig_center
hide everything, pk_7A_label

# ---------- 添加 "7 Å" 标签 ----------
set label_position, [0, -2, 0]
pseudoatom label_7A, panel_left and resn 0LI, label="Stage 1: 7 A cutoff"
set label_color, blue, label_7A
set label_size, 18, label_7A


# ============================================================
# 右图: Stage-2 Graph Construction (10 Å)
# ============================================================
create panel_right, full_protein
hide everything, panel_right

# 全蛋白 cartoon (浅灰)
select right_protein, panel_right and polymer.protein
show cartoon, right_protein
color gray80, right_protein
set cartoon_transparency, 0.80, panel_right

# 配体 (黄色 sticks)
select right_ligand, panel_right and resn 0LI
show sticks, right_ligand
color yellow, right_ligand
set stick_radius, 0.20, right_ligand

# 7A pocket (cyan sticks, 保持可见作为内层)
select right_pocket_7A, panel_right and polymer.protein within 7.0 of (panel_right and resn 0LI)
select right_pocket_7A, byres right_pocket_7A
show sticks, right_pocket_7A
color cyan, right_pocket_7A

# 10A 扩展区域 (绿色半透明 surface)
select right_graph_10A, panel_right and polymer.protein within 10.0 of (panel_right and resn 0LI)
select right_graph_10A, byres right_graph_10A
show surface, right_graph_10A
color palegreen, right_graph_10A
set surface_transparency, 0.55, right_graph_10A

# 同时用 lines 显示 10A 残基骨架
select right_10A_only, right_graph_10A and not right_pocket_7A
show lines, right_10A_only
color palegreen, right_10A_only

# 标注
pseudoatom label_10A, panel_right and resn 0LI, label="Stage 2: 10 A cutoff"
set label_color, forest, label_10A
set label_size, 18, label_10A

# 标注关键残基
select right_label_res, right_pocket_7A and name CA
label right_label_res, "%s%s" % (resn, resi)

# ============================================================
# 6. 布局: 左右并排
# ============================================================
hide everything, full_protein

# 平移右图使之不重叠
translate [40, 0, 0], panel_right

# 调整视角
zoom visible
turn y, 0
orient visible

# ============================================================
# 7. 渲染输出
# ============================================================
viewport 2400, 1000
ray 2400, 1000
png ../images/pocket_preparation_3w2o.png, dpi=300

print("=== Done! Output: ../images/pocket_preparation_3w2o.png ===")
quit
