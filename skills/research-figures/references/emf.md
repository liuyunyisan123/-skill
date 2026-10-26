# EMF制作与核验

仅在当前任务要求EMF、Windows Office矢量图片或取消组合测试时读取。其他科研图按用户或期刊指定的SVG、PDF、EPS等格式制作，不强制生成EMF。

## 优先采用有效矢量源

先检查原始Python绘图程序、PPT原生图形及SVG，选择能保持几何和文字的导出路径。转换前确认源文件中没有把所要求的曲线、网络迹线或图表整体嵌成位图。

专利附图默认以可编辑PPTX为修改源，按[可编辑PPTX与EMF导出](pptx-and-emf.md)选择整图对象范围进行导出。PPTX保存修改能力，EMF用于插入文档；生成EMF不能代替保留PPTX和数据来源。

Inkscape可用时，可按其实际安装位置调用命令行，例如：

```powershell
& $inkscapeExe $svgPath --export-type=emf --export-filename=$emfPath
```

先用当前版本的帮助信息确认导出参数。保留文本版SVG及生成程序。将文字转为轮廓可能提高字体兼容性，但会失去按字符串修改的能力；按本次编辑要求选择，并在报告中准确说明。

Inkscape不可用时，可采用PPT原生图形导出或经过核验的Windows GDI矢量路径。可导出不等于转换正确，不能用PNG截图封装成EMF满足矢量要求。软件确实不可用时保留有效源文件并报告未满足的格式项目，不声称完成不存在的EMF。

## Windows原生导出的实际兼容问题

以下是可能出现的问题及处理方向，不是每次导出都必须执行的步骤：

- DPI缩放可能使图幅与EMF物理边界不一致。统一逻辑坐标、设备映射和frame单位，必要时处理线程DPI感知，并同时检查独立EMF和Office显示。
- 部分PowerPoint导入器不能取消组合包含自定义虚线画笔的EMF。可将虚线和点线按原相位展开为显式矢量子路径；SVG继续保留可整体调整的线型属性。
- PowerPoint取消组合后可能忽略GDI裁剪记录。局部线段可按原可见范围进行几何裁剪，保留原始完整数据，确保取消组合后不延伸出图框。曲线跨越裁剪边界时应正确处理曲线裁剪，不擅自改成低精度折线。
- Word显示正常不保证PowerPoint取消组合后的文字正常。检查字符集、字体及Unicode内容；原生GDI需要时分别采用适合中文和希腊字母的字符集。不要把旧符号字体的编码直接当作Unicode，角度符号应确认实际为°。
- 旋转文字可能在取消组合后丢失世界变换。可采用字体旋转或Office原生旋转文本对象等有效方式，核对旋转方向、位置和基线。

每次处理都应保持科学数据、概率值及实际几何不变；可见范围裁剪和线型拆分只用于显示与兼容。

## 逐文件结构检查

使用随附脚本检查EMF头、记录边界、位图操作、文字和路径记录：

```powershell
python scripts/audit_emf.py figure1.emf figure2.emf --out emf-audit.json --require-pure-vector
```

脚本仅使用Python标准库。可传入多个EMF路径或包含EMF的目录。`--require-pure-vector`只在结构证据支持时通过；遇到经典位图操作、EMF+图像对象、无法判明的GDI注释或像素绘制会给出问题或待检查标记。

脚本检查BITBLT、STRETCHBLT、SETDIBITS、STRETCHDIBITS、ALPHABLEND、TRANSPARENTBLT等记录，也检查扩展画笔的位图画刷载荷，不将“记录中有路径”当作没有位图的证明。脚本不覆盖全部EMF+嵌套资源，发现EMF+、OpenGL或escape载荷时默认标记待进一步核验，不直接判为纯矢量；补充人工解析后才能判断，不能把未知项当作通过。

需要扩展解析时，查阅微软的[EMR_EXTCREATEPEN记录定义](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-emf/d7f51e05-4024-497c-ad4a-8aeca9d34256)和[EmfPlusImage对象定义](https://learn.microsoft.com/de-de/openspecs/windows_protocols/ms-emfplus/02c80141-208e-4335-ad51-190b40a1802c)，按实际字段检查嵌入图像。

结构检查不能证明字体正确、图形没有裁切，也不能证明PowerPoint可编辑，后续视觉和Office测试仍需执行。

## PowerPoint与视觉核验

在独立的Windows PowerPoint会话或任务副本中插入每个EMF，测试取消组合。某些图片需要先转换为绘图对象，再进行第二次取消组合；应确认最终对象类型，而不只记录调用未报错。

分别检查独立文字、线段或自由图形，实测一处文字编辑及一处几何或线条属性编辑，并恢复测试值。记录PowerPoint版本、对象数量、图片对象残留、测试结果和失败原因。图表中的自由图形不等于带数据表的原生图表，复合数学标注也不等于单个原生公式。

检查取消组合前后的全部图件，重点查看希腊字母、度符号、箭头、旋转轴标题、上下标、局部图边界、虚线点线及误差棒。能取消组合但文字乱码或几何外泄仍不满足要求。无法测试时明确未测试；失败时记录具体原因和可编辑源文件的替代修改方法，不声称完全可编辑。

以较大倍率重新渲染矢量细节，确认线条和文字清晰。放大一张低分辨率预览不能作为EMF放大核验。若生成检查用PDF，可检查图件是否仍为矢量；其结果是附加证据，不代替EMF内部检查。
