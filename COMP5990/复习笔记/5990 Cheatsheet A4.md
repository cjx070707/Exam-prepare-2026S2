# INFO5990 — Cheatsheet A4（打印版）

> **2 页 A4 PDF**，考前打印用。内容与 [[5990 必背速查]] 同源，版式为双栏速查表。

| 文件 | 用途 |
|------|------|
| **`5990 Cheatsheet A4.pdf`** | 打印（推荐） |
| `5990 Cheatsheet A4.html` | 源文件；改内容后重新导出 PDF |

## 重新导出 PDF

在仓库根目录执行：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="COMP5990/复习笔记/5990 Cheatsheet A4.pdf" \
  "file://$(pwd)/COMP5990/复习笔记/5990 Cheatsheet A4.html"
```

## 覆盖范围

- Page 1：答题骨架 · 价值/项目 · 沟通 · 治理/变革 · 估算 · 通用句库
- Page 2：CIA/漏洞/NIST/STRIDE/Data lifecycle · IR/DR/BCP · 质量/伦理 · Q8–Q11 句库

详情：[[第一组 专业实践与组织价值]] · [[第二组 项目生命周期与估算]] · [[第三组 沟通协作、治理与变革]] · [[第四组 安全、质量与伦理]] · [[5990 复习笔记]]
