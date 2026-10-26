# 中文科研写作 附图与汇报 Skills

三个可分别安装的 Codex 技能，用于中文科研文字写作、科研附图和学术汇报。重点是讲清研究意义、方法和结果，让内容准确、逻辑顺畅、容易理解，并保持统一的文字、图件和演示格式。

## 包含的技能

| 技能 | 用途 | 调用方式 |
| --- | --- | --- |
| [科研写作](skills/research-writing/SKILL.md) | 撰写、修改或审阅中文论文、专利说明书和权利要求书；规范 Word 字体、变量和公式 | `$research-writing` |
| [科研汇报PPT](skills/academic-ppt/SKILL.md) | 制作、修改或规划组会、研究进展、论文及专利研究汇报 | `$academic-ppt` |
| [科研附图](skills/research-figures/SKILL.md) | 绘制科研矢量图，规范变量斜体，保留源文件；按需生成EMF、插入Word及核验PowerPoint编辑能力 | `$research-figures` |

三个技能可以独立使用，也可配合使用。科研写作负责文字与文档，科研附图负责图件制作与核验，科研汇报PPT负责汇报逻辑与幻灯片排版。

## 主要规则

### 科研写作

- 按“研究为什么重要 → 已有方法 → 具体不足 → 本研究的方法 → 结果与意义”组织内容。
- 专利背景按已有方法的能力递进引出具体技术缺口；先补足因果，再合并重复解释，将本申请的具体步骤、参数和评价留给后文。
- 使用自然、准确的科研用语，避免生造名词、空泛表述和没有依据的结论。
- 根据实际代码、数据和资料写作，不编造结果或参考文献。
- 默认中文标题用黑体，正文用宋体、小四；字母、数字和希腊数学符号用 Times New Roman（新罗马字体）。
- 表格内容及表头统一用五号（10.5 磅）；中文用宋体，字母、数字和希腊数学符号用 Times New Roman。
- 正文数学变量用斜体，下标和上标使用真正的格式标记。
- 仅独立成行的公式使用可编辑的 MathType 对象；正文中的简短公式和变量保留为普通可编辑文本。
- 如果要求“保留原格式”，按原文档格式修改；用户的当前要求和指定格式优先于默认规则。

### 科研汇报PPT

- 简洁的学术风格，图多字少，突出研究的逻辑、作用、方法和结果。
- 默认白色背景，统一对齐和留白；文字颜色以深灰或黑色为主，强调色用于有实际意义的区分。
- 中文用微软雅黑；字母、数字和希腊数学符号用 Times New Roman。
- 所有可见文字至少 18 磅，包括图例、坐标轴、表格、图注和页码；图片中的文字也按最终显示大小检查。
- 避免堆砌数字和复杂推导；详细参数和补充解释可以放入备注，影响结论的重要条件仍在页面中说明。
- 页数根据内容确定，不固定套用某一份汇报；仅请求大纲时，只提供大纲。

### 科研附图

- 根据当前真实数据、概率函数、模型结果和原始绘图程序制作，不因格式修改重新计算或调整实验结果。
- 优先使用Python、PPT原生图形或SVG；网络迹线、流程框、曲线和误差棒等按矢量方式输出。
- 默认白底黑白，以实线、虚线、点线和标记区分对象；当前用户和期刊规范优先。
- 专利说明书附图默认采用随附PPT参考的竖版、一图一页格式，以原生文字、线条和路径保留修改能力；页数和子图数量按实际内容确定。
- 以可编辑PPTX作为主修改源，按需导出EMF用于插入文档；数据图保留数据及绘图程序，区分修改图形与修改数据。
- 数学变量用斜体，规范中西文字体、希腊字母、上下标和单位，精简图内冗余解释。
- 保留并交付可编辑源文件；EMF内部位图检查与PowerPoint实际取消组合测试分别核验。
- 插入Word时保留指定模板并逐页渲染检查；按需提供格式核验报告。

## 目录结构

```text
research-skills/
├── README.md
├── .gitignore
└── skills/
    ├── research-writing/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/
    │       ├── background.md
    │       ├── paper.md
    │       ├── patent.md
    │       └── word-formatting.md
    ├── academic-ppt/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/
    │       ├── design-and-checks.md
    │       └── narrative.md
    └── research-figures/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        │   └── patent-figures-reference.pptx
        ├── references/
        │   ├── design.md
        │   ├── emf.md
        │   ├── pptx-and-emf.md
        │   └── word-and-delivery.md
        └── scripts/
            └── audit_emf.py
```

`SKILL.md` 是技能入口，`references/` 保存按任务使用的详细规则，`agents/openai.yaml` 提供显示名称和默认提示。

## 安装

1. 下载或克隆本仓库。
2. 打开仓库的 `skills` 文件夹，将其中需要使用的 `research-writing`、`research-figures` 和 `academic-ppt` 文件夹完整复制到 Codex 的用户技能目录。
3. 如果目标目录已有同名技能，先备份原版本，再决定是否替换。
4. 在 Codex 中用下面的名称调用。如果当前对话未识别新安装的技能，可重新打开 Codex 并新建对话。

默认用户技能目录：

| 系统 | 目录 |
| --- | --- |
| Windows | `%USERPROFILE%\.codex\skills\` |
| macOS / Linux | `~/.codex/skills/` |
| 设置了 `CODEX_HOME` 的环境 | `CODEX_HOME` 指向目录下的 `skills/` |

Windows 默认安装后的路径应为：

```text
C:\Users\你的用户名\.codex\skills\research-writing\SKILL.md
C:\Users\你的用户名\.codex\skills\academic-ppt\SKILL.md
C:\Users\你的用户名\.codex\skills\research-figures\SKILL.md
```

请复制相应技能文件夹本身，并保留其内部文件；不要把整个仓库外层文件夹当作一个技能安装。

## 使用示例

修改专利文件：

```text
使用 $research-writing 根据我提供的代码、数据和旧稿，修改专利说明书和权利要求书，保留原格式。
```

重写论文引言：

```text
使用 $research-writing 重写论文引言，突出研究的实际作用、现有方法不足和本文切入点。
```

制作组会汇报：

```text
使用 $academic-ppt 根据研究资料制作组会PPT，突出意义、方法和结果，图多字少。
```

只规划大纲：

```text
使用 $academic-ppt 先给我10页汇报大纲，不生成PPT文件。
```

制作专利附图：

```text
使用 $research-figures 根据我的原始程序和实验结果制作黑白专利附图，沿用随附PPT参考格式，以可编辑PPTX作为主修改源，变量用斜体，按需导出EMF并核验显示和编辑能力。
```

使用时提供相关资料的路径，并说明受众、研究阶段和需要保留的格式。涉及模型结果时，提供当前代码和数据，便于核对结论与图表。

## 工具要求

这三个技能提供写作、绘图与排版指令。实际生成、编辑和检查 Word 或 PPT 文件，需要运行环境提供相应文档与演示工具；技能本身不附带这些软件。科研附图提供仅依赖Python标准库的EMF记录检查脚本；实际转换和PowerPoint测试仍需可用的矢量及Office工具。

制作真正可编辑的 MathType 公式，需要可用的 MathType 及相应编辑能力。公式图片、LaTeX 文本和 Word 原生公式不能冒充 MathType 对象。使用指定字体时，运行环境应安装对应字体。

## 上传到 GitHub

在 GitHub 创建仓库后，将本文件夹中的 `README.md`、`.gitignore` 和 `skills/` 上传到仓库根目录，保持目录结构。无需上传当前研究项目的代码、数据、专利文件或汇报文件。

更新已有仓库时，在仓库页面选择 **Add file → Upload files**，拖入本文件夹内的文件和 `skills/` 目录，核对相同路径的修改，再选择 **Commit changes**。如果仓库将这三个技能直接放在根目录，则只更新对应技能目录，保持原路径。

本地安装与GitHub仓库互相独立：运行安装脚本后，仍需另行上传并提交仓库更改。后续只修改本地技能不会自动更新GitHub。

科研附图技能包含用户指定的真实专利附图PPT作为格式参考；公开仓库会一并公开其中的图形、参数和结果。准备公开分享时，应先决定保留该示例，还是替换成不含实际研究内容的格式样例；替换时同步核对技能中的参考路径。

## 修改规则

通用规则写在各技能的 `SKILL.md` 中，专项说明写在对应的 `references/` 中。修改技能名称或用途时，同时检查 `agents/openai.yaml` 和本 README 中的调用示例。
