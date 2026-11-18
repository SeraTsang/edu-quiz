# 教综解析 → 辨析题 Skill

用途：从教综试题解析（没有题干也可以）中自动识别模糊点、易错点，生成高质量判断式辨析题与独立考点、针对性解析、记忆点。匹配现有 edu-quiz 网站导入格式。

## 安装到 Codex 项目

将整个 `edu-quiz-analyzer` 文件夹复制到项目目录：

```text
C:\github\edu-quiz\.agents\skills\edu-quiz-analyzer\
  SKILL.md
  README.md
  examples\
  scripts\
```

对应 Git Bash 路径：`/c/github/edu-quiz/.agents/skills/edu-quiz-analyzer/SKILL.md`。根据实际使用的 Agent/Codex 环境重新载入项目或开启新会话，让其发现 Skill。普通 ChatGPT 对话并不会因为 Git 项目中存在该文件而自动读取；可上传 `SKILL.md` 并明确说“按照这个 Skill 处理下面解析”。

## 最简使用方法

在支持 Skill 的 Codex 会话中输入：

```text
使用 edu-quiz-analyzer，按默认“粘贴”格式，把以下教综原题解析整理成辨析题。只有解析，没有原题。请提炼易错点与针对性拓展，默认每个考点生成 2–3 道，最后输出能直接粘到网站的代码块：

[在这里粘贴原解析]
```

输出包括简短“易错点速览”和一整个**五字段可复制代码块**。每题的字段为：`【考点】`、`【题干】`、`【解析】`、`【记忆点】`、`【判定】`。只复制代码块内容，在网站「录入新题 / 导入章节」粘贴、点“解析文本”，**逐题确认正确/错误**后入库。

## 需要 JSON 章节包时

```text
使用 edu-quiz-analyzer。格式：JSON章节包。章节：教育学 · 第一章。题数：6。把下面解析生成辨析题和独立记忆点，并保存为 UTF-8 JSON 文件：

[粘贴原解析]
```

JSON 包可在网站「更多 → 数据迁移 → 导入章节包 / 备份」导入；此操作会**新增**章节，名称相同也会产生另一个章节。若需向已存在的章节追加题目，优先用默认文本粘贴导入。

## 重要限制

1. 原选择题的“故选 A/B/C/D”不等于新辨析题答案。新题要单独验证真假。
2. 请使用已升级的 `index_考点记忆点修复.html`（替换部署时命名为 `index.html`）。它会识别独立的 `【考点】`、`【记忆点】`、`【判定】`，且不会把这些字段留在解析正文。
3. 老版本网站可能会把考点/记忆点混入解析，**仅更换 Skill 无法修复旧网页解析器**。新版 JSON 导入支持 `g`（考点）与 `k`（记忆点）。
4. 生成前建议提供具体教材或地方考试体系（若有），避免不同教材的分类口径冲突。

## 简单格式检查

```bash
python scripts/check_quiz.py examples/site-paste.txt
python scripts/check_quiz.py examples/chapter-import.json
```

通过检查只代表格式兼容，不代表教综知识点一定正确。请复核内容和答案。
