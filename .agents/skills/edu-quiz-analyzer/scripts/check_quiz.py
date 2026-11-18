#!/usr/bin/env python3
"""Offline structural checker for edu-quiz analyzer output. No third-party dependencies."""
import json
import re
import sys
from pathlib import Path


def check_text(path):
    text = path.read_text(encoding="utf-8-sig").strip()
    blocks = re.split(r"\n[ \t]*\n", text)
    errors = []
    labels = ["考点", "题干", "解析", "记忆点", "判定"]
    for i, block in enumerate(blocks, 1):
        lines = block.splitlines()
        positions = []
        for label in labels:
            idx = [j for j, line in enumerate(lines) if line.startswith(f"【{label}】")]
            if len(idx) != 1:
                errors.append(f"第{i}题应有且仅有一个【{label}】行")
                continue
            positions.append(idx[0])
            if not lines[idx[0]].split("】",1)[1].strip():
                errors.append(f"第{i}题【{label}】不能为空")
        if len(positions) == 5 and positions != sorted(positions):
            errors.append(f"第{i}题字段必须依次为："+"、".join(labels))
        if not lines or lines[-1] not in ("【判定】正确", "【判定】错误"):
            errors.append(f"第{i}题末行必须为【判定】正确 或【判定】错误")
    return len(blocks), errors


def check_json(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    errors = []
    cs = data.get("chapters")
    if not isinstance(cs, list) or not cs:
        return 0, ["chapters 必须是非空数组"]
    count = 0
    for i, ch in enumerate(cs, 1):
        if not isinstance(ch, dict) or not isinstance(ch.get("name"), str) or not ch["name"].strip():
            errors.append(f"第{i}章缺少有效 name")
            continue
        if not isinstance(ch.get("qs"), list) or not ch["qs"]:
            errors.append(f"第{i}章缺少非空 qs")
            continue
        for j, q in enumerate(ch["qs"], 1):
            count += 1
            if not isinstance(q, dict):
                errors.append(f"第{i}章第{j}题不是对象")
                continue
            for key in ("s", "x", "k", "g"):
                if not isinstance(q.get(key), str) or not q[key].strip():
                    errors.append(f"第{i}章第{j}题缺少非空 {key}")
            if type(q.get("a")) is not bool:
                errors.append(f"第{i}章第{j}题 a 必须是 JSON 布尔值 true/false")
    return count, errors


def main():
    if len(sys.argv) != 2:
        sys.exit("用法: python check_quiz.py <题目.txt 或 章节.json>")
    path = Path(sys.argv[1])
    try:
        count, errors = (check_json(path) if path.suffix.lower() == ".json" else check_text(path))
    except (OSError, ValueError, UnicodeError) as exc:
        sys.exit(f"读取或解析失败: {exc}")
    if errors:
        print("格式检查失败：\n" + "\n".join("- " + x for x in errors))
        sys.exit(1)
    print(f"格式检查通过：共 {count} 题。注意仍须人工复核真假和知识准确性。")


if __name__ == "__main__":
    main()
