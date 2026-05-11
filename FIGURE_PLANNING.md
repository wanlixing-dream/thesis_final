# 毕业论文图表规划指南

## 📋 论文结构概览

根据你的论文结构，主要章节如下：

1. **第1章：前言**
   - 课题研究背景及意义
   - 国内外研究现状
   - 本文主要研究内容

2. **第2章：相关技术与理论基础**
   - 图神经网络与Graph-Transformer
   - 多任务学习理论
   - 分子对接与打分函数
   - 混合密度网络

3. **第3章：InterMoBA-MTL系统设计** ⭐
   - 系统总体架构
   - Graph-Transformer主干网络
   - 多任务学习框架设计
   - 损失函数与权重调度

4. **第4章：可解释能量建模方法**
   - 四分量混合高斯模型
   - 原子对类型掩蔽机制
   - 几何约束设计
   - 能量分解与可视化

5. **第5章：对接评测管线设计**
   - Monte Carlo采样策略
   - BFGS局部优化
   - RMSD聚类
   - 评测指标

---

## 🎯 系统架构图位置规划

### 主要位置：第3章第1节"系统总体架构"

**位置**：`content/content.tex` 第3章第1节

**代码位置**：
```latex
\section{InterMoBA-MTL系统设计}
\subsection{系统总体架构}

InterMoBA-MTL系统的总体架构如图3-1所示。系统采用编码器-解码器结构...

% TODO: 插入系统架构图
% \begin{figure}[hbt]
%     \centering
%     \includegraphics[width=0.9\textwidth]{images/system_architecture.png}
%     \caption{InterMoBA-MTL系统总体架构}
%     \label{F.system_architecture}
% \end{figure}
```

**建议操作**：
1. 将架构图文件复制到 `images/` 目录
2. 取消注释上述代码块
3. 根据实际文件名修改图片路径

---

## 📊 其他图表建议位置

### 第3章：InterMoBA-MTL系统设计

#### 图3-2：MoBA适配器架构图
**位置**：第3章第2节"Graph-Transformer主干网络" - "MoBA适配器"小节
**内容**：展示MoBA适配器的内部结构，包括动态分块、Top-k选择、任务特定处理等

#### 图3-3：多任务学习框架图
**位置**：第3章第3节"多任务学习框架设计"
**内容**：展示三个任务的并行训练流程，包括任务融合策略

#### 图3-4：损失函数权重调度曲线
**位置**：第3章第4节"损失函数与权重调度"
**内容**：展示动态权重调度过程中权重的变化曲线

### 第4章：可解释能量建模方法

#### 图4-1：四分量混合高斯模型示意图
**位置**：第4章第1节"四分量混合高斯模型"
**内容**：展示四个高斯分量如何组合表示不同类型的物理相互作用

#### 图4-2：原子对类型掩蔽机制示意图
**位置**：第4章第2节"原子对类型掩蔽机制"
**内容**：展示不同类型原子对如何激活不同的高斯分量

#### 图4-3：能量分解可视化示例 ⭐
**位置**：第4章第4节"能量分解与可视化"
**代码位置**：
```latex
% TODO: 插入能量分解可视化图
% \begin{figure}[hbt]
%     \centering
%     \includegraphics[width=0.8\textwidth]{images/energy_decomposition.png}
%     \caption{能量分解可视化示例}
%     \label{F.energy_decomposition}
% \end{figure}
```

### 第5章：对接评测管线设计

#### 图5-1：对接流程图
**位置**：第5章开头
**内容**：展示完整的对接流程，包括Monte Carlo采样、BFGS优化、RMSD聚类等步骤

#### 图5-2：评测指标计算流程
**位置**：第5章第4节"评测指标"
**内容**：展示Top-K成功率、AUROC等指标的计算方法

---

## 🔧 具体操作步骤

### 步骤1：准备架构图文件

1. **复制架构图**：
   ```bash
   # 将之前创建的架构图文档转换为图片
   # 或者使用绘图工具重新绘制
   
   # 建议格式：
   # - PNG格式（适合屏幕显示）
   # - PDF格式（适合打印，推荐）
   # - SVG格式（矢量图，可缩放）
   ```

2. **放置到正确位置**：
   ```bash
   # 复制到论文的images目录
   cp architecture_diagram.png /home/wanlixing/桌面/InterMoBA_graduation_project/毕业设计/thesis_final/images/
   ```

### 步骤2：修改LaTeX文件

打开 `content/content.tex`，找到第3章第1节：

```latex
\section{InterMoBA-MTL系统设计}
\subsection{系统总体架构}

InterMoBA-MTL系统的总体架构如图3-1所示。系统采用编码器-解码器结构，核心是一个统一的Graph-Transformer主干网络，负责提取蛋白质-配体复合物的特征表示。在主干网络之上，设计了三个任务特定的输出头：亲和力回归头、姿态选择头和能量预测头。

% 取消注释并修改
\begin{figure}[hbt]
    \centering
    \includegraphics[width=0.9\textwidth]{images/architecture_diagram.pdf}
    \caption{InterMoBA-MTL系统总体架构}
    \label{F.system_architecture}
\end{figure}
```

### 步骤3：编译论文

```bash
cd /home/wanlixing/桌面/InterMoBA_graduation_project/毕业设计/thesis_final
make
# 或者
xelatex sztuthesis_main.tex
```

---

## 📐 图表设计建议

### 系统架构图设计要点

1. **层次清晰**：
   - 输入层 → 特征提取层 → MoBA注意力层 → 编码器层 → 多任务输出层 → 损失函数层

2. **模块化展示**：
   - 每个模块用不同颜色区分
   - 使用箭头表示数据流向
   - 标注关键组件名称

3. **信息完整**：
   - 包含所有关键组件
   - 标注输入输出
   - 注释关键技术点

4. **美观专业**：
   - 使用统一的配色方案
   - 保持字体大小一致
   - 确保打印效果清晰

### 推荐工具

1. **专业绘图工具**：
   - Draw.io（免费，在线）
   - Visio（微软）
   - Lucidchart（在线）
   - Adobe Illustrator（专业）

2. **LaTeX绘图**：
   - TikZ（代码绘制，推荐）
   - PGFPlots（数据可视化）

3. **Python绘图**：
   - Matplotlib
   - Graphviz
   - NetworkX

---

## 🎨 图表编号规范

根据论文模板设置，图表按章节编号：

- 图3-1：第3章第1个图
- 图3-2：第3章第2个图
- 图4-1：第4章第1个图
- 图5-1：第5章第1个图

**LaTeX自动编号**：
```latex
\begin{figure}[hbt]
    \centering
    \includegraphics[width=0.9\textwidth]{images/xxx.png}
    \caption{图表标题}  % 自动编号为"图X-Y"
    \label{F.xxx}
\end{figure}
```

**引用方式**：
```latex
如图\ref{F.system_architecture}所示...
```

---

## 📝 图表标题规范

### 中文标题格式
- 简洁明了，不超过20字
- 使用名词性短语
- 不使用标点符号

**示例**：
- ✅ InterMoBA-MTL系统总体架构
- ✅ 四分量混合高斯模型示意图
- ✅ 能量分解可视化示例
- ❌ 图3-1：系统架构图（不要在标题中包含编号）

### 英文标题格式（如需要）
- 首字母大写
- 使用名词性短语
- 不使用标点符号

**示例**：
- ✅ Overall Architecture of InterMoBA-MTL System
- ✅ Four-Component Gaussian Mixture Model

---

## 🚀 快速实施计划

### 今天（2026-04-12）

1. **准备系统架构图**：
   - [ ] 使用绘图工具绘制架构图
   - [ ] 导出为PDF格式
   - [ ] 放置到 `images/` 目录

2. **修改论文**：
   - [ ] 取消注释架构图代码
   - [ ] 调整图片大小和位置
   - [ ] 编译查看效果

### 明天

3. **准备其他图表**：
   - [ ] MoBA适配器架构图
   - [ ] 多任务学习框架图
   - [ ] 能量分解可视化图

4. **完善论文**：
   - [ ] 检查所有图表引用
   - [ ] 确保图表编号正确
   - [ ] 最终编译和检查

---

## 📚 参考资料

### LaTeX图表相关命令

```latex
% 图片基本插入
\begin{figure}[hbt]
    \centering
    \includegraphics[width=0.9\textwidth]{images/xxx.png}
    \caption{图表标题}
    \label{F.xxx}
\end{figure}

% 图片位置参数
% h: here（当前位置）
% t: top（页顶）
% b: bottom（页底）
% p: page（单独一页）

% 图片大小调整
\includegraphics[width=0.9\textwidth]{xxx.png}  % 相对宽度
\includegraphics[width=10cm]{xxx.png}           % 绝对宽度
\includegraphics[scale=0.5]{xxx.png}            % 缩放比例

% 多图并排
\begin{figure}[hbt]
    \centering
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{xxx1.png}
        \caption{图1}
    \end{minipage}
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{xxx2.png}
        \caption{图2}
    \end{minipage}
\end{figure}
```

---

## ✅ 检查清单

在提交论文前，请检查以下内容：

### 图表内容
- [ ] 所有图表都有标题
- [ ] 所有图表都有标签（\label）
- [ ] 所有图表都在正文中被引用
- [ ] 图表编号连续无遗漏
- [ ] 图表内容清晰可读

### 图表质量
- [ ] 图片分辨率足够（至少300dpi）
- [ ] 字体大小适中
- [ ] 颜色对比度良好
- [ ] 打印效果清晰

### 格式规范
- [ ] 图表标题格式统一
- [ ] 图表位置合理
- [ ] 图表引用格式正确
- [ ] 编译无错误警告

---

**规划文档**：`/home/wanlixing/桌面/InterMoBA_graduation_project/毕业设计/thesis_final/FIGURE_PLANNING.md`
**创建时间**：2026-04-12
