#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISO 9001:2026 升版辅导网页报告生成器

读取一份 JSON 格式的差距分析与升版建议结果，基于 assets/report_template.html
模板生成一份美观的 HTML 网页报告（含运行改进、文件变更、执行计划）。

用法:
    python scripts/generate_report.py --input analysis.json --output report.html

JSON 输入结构:
{
  "title": "报告标题",
  "company": "组织名称",
  "scope": "体系范围",
  "date": "报告日期(YYYY-MM-DD)",
  "reviewer": "编制角色",
  "overview": "报告摘要(页面头条副标题)",
  "summary_note": "差距总览段落文字",
  "change_points": [
    {
      "clause": "4.1",
      "title": "变更点名",
      "interpretation": "2026版要求解读",
      "status": "good | partial | gap",
      "status_label": "基本符合/部分符合/存在差距"
    }
  ],
  "running_improvements": [
    {"title": "建议标题", "detail": "针对运行现状的改进建议"}
  ],
  "document_changes": [
    {"source": "现有文件", "action": "新增/修订/删除", "target": "变更后文件/说明"}
  ],
  "plan": [
    {
      "phase": "阶段名称",
      "timeline": "时间窗",
      "tasks": ["任务1", "任务2"],
      "owner": "责任人",
      "deliverables": "交付物"
    }
  ]
}
"""
import argparse
import json
import sys
import os


def _status_badge(status):
    """返回状态徽章的 HTML。"""
    mapping = {
        "good": ("st-good", "基本符合"),
        "partial": ("st-partial", "部分符合"),
        "gap": ("st-gap", "存在差距"),
    }
    cls, _label = mapping.get(status, ("st-partial", "部分符合"))
    return cls


def _html_escape(text):
    if text is None:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def build_change_point_rows(items):
    rows = []
    for item in items or []:
        clause = _html_escape(item.get("clause", ""))
        title = _html_escape(item.get("title", ""))
        interp = _html_escape(item.get("interpretation", ""))
        status = item.get("status", "partial")
        label = _html_escape(item.get("status_label", ""))
        if not label:
            label = {"good": "基本符合", "partial": "部分符合", "gap": "存在差距"}.get(status, "部分符合")
        badge = '<span class="status %s" data-status="%s">%s</span>' % (
            _status_badge(status), _html_escape(status), label)
        rows.append(
            "<tr>"
            "<td><span class=\"tag\">%s</span>%s</td>"
            "<td><b>%s</b></td>"
            "<td>%s</td>"
            "<td>%s</td>"
            "</tr>" % (clause, "", title, interp, badge)
        )
    return "\n".join(rows)


def build_improvement_items(items):
    lis = []
    for idx, item in enumerate(items or [], start=1):
        title = _html_escape(item.get("title", ""))
        detail = _html_escape(item.get("detail", ""))
        lis.append(
            "<li><b>%d. %s</b><br>%s</li>" % (idx, title, detail)
        )
    return "\n".join(lis)


def build_doc_change_rows(items):
    out = []
    if not items:
        return '<p>（无文件变更项，或需补充体系文件清单后确定）</p>'
    for item in items:
        source = _html_escape(item.get("source", ""))
        action = _html_escape(item.get("action", ""))
        target = _html_escape(item.get("target", ""))
        action_block = ('<span class="tag">%s</span>' % action) if action else ""
        out.append(
            '<div class="doc-row">'
            '<div class="src">%s</div>'
            '<div class="arrow">&#10132;</div>'
            '<div class="dst">%s %s</div>'
            '</div>' % (source, action_block, target)
        )
    return "\n".join(out)


def build_plan_phases(phases):
    blocks = []
    for phase in phases or []:
        name = _html_escape(phase.get("phase", ""))
        timeline = _html_escape(phase.get("timeline", ""))
        owner = _html_escape(phase.get("owner", ""))
        deliverables = _html_escape(phase.get("deliverables", ""))
        tasks = phase.get("tasks", [])
        task_lis = "\n".join(
            "<li>%s</li>" % _html_escape(t) for t in tasks
        )
        owner_line = ('<div class="owner">责任主体：%s</div>' % owner) if owner else ""
        dl_line = ('<div class="owner">交付物：%s</div>' % deliverables) if deliverables else ""
        blocks.append(
            '<div class="phase">'
            '<div class="phase-head"><span class="name">%s</span><span class="time">%s</span></div>'
            '<div class="phase-body"><ul class="clean">%s</ul>%s%s</div>'
            '</div>' % (name, timeline, task_lis, owner_line, dl_line)
        )
    return "\n".join(blocks)


def main():
    parser = argparse.ArgumentParser(description="生成 ISO 9001:2026 升版辅导网页报告")
    parser.add_argument("--input", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出 HTML 文件路径")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit("输入文件不存在: %s" % args.input)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 校验必填字段
    for key in ("change_points",):
        if key not in data:
            sys.exit("输入 JSON 缺少必填字段: %s" % key)

    change_points = data.get("change_points", [])
    if not isinstance(change_points, list):
        sys.exit("change_points 必须是数组")

    counts = {"good": 0, "partial": 0, "gap": 0}
    for cp in change_points:
        status = cp.get("status", "partial")
        if status in counts:
            counts[status] += 1
        else:
            counts[status] = 0

    # 模板路径：脚本位于 <skill>/scripts/，模板位于 <skill>/assets/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "..", "assets", "report_template.html")
    if not os.path.exists(template_path):
        sys.exit("模板文件不存在: %s" % template_path)
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    replacements = {
        "__REPORT_TITLE__": _html_escape(data.get("title", "ISO 9001:2026 质量管理体系升版辅导报告")),
        "__OVERVIEW__": _html_escape(data.get("overview", "")),
        "__COMPANY__": _html_escape(data.get("company", "")),
        "__SCOPE__": _html_escape(data.get("scope", "")),
        "__DATE__": _html_escape(data.get("date", "")),
        "__REVIEWER__": _html_escape(data.get("reviewer", "")),
        "__SUMMARY_NOTE__": _html_escape(data.get("summary_note", "")),
        "__CNT_GOOD__": str(counts["good"]),
        "__CNT_PARTIAL__": str(counts["partial"]),
        "__CNT_GAP__": str(counts["gap"]),
        "__CNT_TOTAL__": str(len(change_points)),
        "__CHANGE_POINTS_ROWS__": build_change_point_rows(change_points),
        "__RUNNING_IMPROVEMENTS_ITEMS__": build_improvement_items(data.get("running_improvements", [])),
        "__DOC_CHANGES_ROWS__": build_doc_change_rows(data.get("document_changes", [])),
        "__PLAN_PHASES__": build_plan_phases(data.get("plan", [])),
    }

    for token, value in replacements.items():
        if token in html:
            html = html.replace(token, value)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    result = {
        "status": "success",
        "output": args.output,
        "size_bytes": os.path.getsize(args.output),
        "summary": {
            "total": len(change_points),
            "good": counts["good"],
            "partial": counts["partial"],
            "gap": counts["gap"],
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()