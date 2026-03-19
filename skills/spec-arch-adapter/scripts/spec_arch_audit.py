#!/usr/bin/env python3
import argparse
import fnmatch
import json
import os
import re
from datetime import datetime

SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LANGUAGE_FILES = {
    "Python": ["requirements.txt", "pyproject.toml", "setup.py"],
    "Node": ["package.json"],
    "Go": ["go.mod"],
    "Rust": ["Cargo.toml"],
    "Java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    ".NET": ["*.csproj", "*.sln"],
    "Ruby": ["Gemfile"],
    "PHP": ["composer.json"],
    "Swift": ["Package.swift"],
}

ENTRYPOINT_CANDIDATES = [
    "src/main.py",
    "src/app.py",
    "main.py",
    "app.py",
    "src/index.js",
    "src/index.ts",
    "index.js",
    "index.ts",
    "src/main.go",
    "main.go",
    "cmd/main.go",
    "src/main.rs",
    "src/lib.rs",
    "src/Main.java",
    "src/main/java/Main.java",
    "src/Program.cs",
    "Program.cs",
]

DEFAULT_MODULE_DIRS = [
    "config",
    "src/config",
    "src/core",
    "src/data",
    "src/monitor",
    "src/servers",
    "src/utils",
    "src/data/bet365",
    "src/data/pinnacle",
]

PITFALLS_TEMPLATE = """摘要：活跃坑位索引（完整 RCA 与历史快照见 `docs/qa/pitfalls_archive/`）。
# Pitfalls
## 写入规则

- `pitfalls.md` 只保留会影响当前编码判断的 ACTIVE 卡片，不再保存长篇事故流水账。
- Bugfix 回合优先更新同根因的现有 ACTIVE 卡片；只有新根因才新增卡片。
- 同根因复发时，更新 `Last seen`、`Rule`、`Guardrail`、`Canonical detail`，不要再追加重复 section。
- 完整 RCA 写入 `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md` 或对应 Sprint close 文档，再把路径回链到 ACTIVE 卡片。
- ACTIVE 卡片必填字段：`Scope`、`Search keywords`、`Rule`、`Guardrail`、`Last seen`、`Canonical detail`、`Archive when`。
- 严禁敏感信息：不要写账号/密码/cookie/token。

## 活跃游标与归档规则

- 主文件预算：总长度目标 `<= 250` 行；ACTIVE 卡片 `<= 10` 张。
- 必须执行归档的触发条件：Sprint close、主文件超过 250 行、ACTIVE 卡片超过 10 张。

## ACTIVE 卡片模板

```markdown
### ACTIVE YYYY-MM-DD <标题>
- Scope: `path/to/file.py`
- Search keywords: `keyword-a`, `keyword-b`
- Rule: 未来编码必须守住的约束/不变量
- Guardrail: `tests/...` 或 close gate
- Last seen: `YYYY-MM-DD`
- Canonical detail: `docs/qa/pitfalls_archive/YYYY-MM-DD[-suffix].md`
- Archive when: 连续 2 个 Sprint close 未命中，且无新证据
```

## 活跃坑位索引

（项目初始化，暂无活跃坑位。首次 bugfix 后在此新增 ACTIVE 卡片。）

## 活跃坑位卡片

（暂无。）
"""

PITFALLS_ARCHIVE_README = """# Pitfalls Archive

完整 RCA（Root Cause Analysis）归档目录。

## 命名规范

`YYYY-MM-DD[-suffix].md`

## 内容要求

每份归档文档应包含：
1. 事故概要
2. 根因分析
3. 修复措施
4. 防回归（测试/门禁）
5. 关联链接
"""

TEMPLATES = {
    "README.md": """# {project_name}\n\n## 项目简介\n请在此补充项目目标与核心功能。\n\n## 检测到的上下文\n- 语言/技术栈：{languages}\n- 入口候选：{entrypoints}\n- 构建清单：{manifests}\n\n## 快速开始（建议）\n{quick_start_cn}\n\n## 文档入口\n- 规则与流程：`AGENTS.md`\n- 文档索引：`docs/README.md`\n- 进度游标：`docs/task/progress.md`\n- 活跃坑位：`docs/qa/pitfalls.md`\n\n## 注意事项\n- 不要提交密钥、Cookie 或日志文件。\n""",
    "README.en.md": """# {project_name}\n\n## Overview\nDescribe the project goal and core functionality.\n\n## Detected Context\n- Languages/Stack: {languages}\n- Entry candidates: {entrypoints}\n- Manifests: {manifests}\n\n## Quick Start (suggested)\n{quick_start_en}\n\n## Docs Entry Points\n- Rules & workflow: `AGENTS.md`\n- Docs index: `docs/README.md`\n- Progress cursor: `docs/task/progress.md`\n- Active pitfalls: `docs/qa/pitfalls.md`\n\n## Notes\n- Do not commit secrets, cookies, or logs.\n""",
    "AGENTS.md": """# Repository Guidelines\n\n本文件聚焦 AI/流程规则。项目概览与运行命令见 `README.md`；文档索引见 `docs/README.md`。\n\n## Project Context\n- Languages: {languages}\n- Entry candidates: {entrypoints}\n- Test commands (suggested): {test_commands}\n\n## Coding Style & Naming Conventions\n- 请补充本项目的语言/风格规范。\n\n## Testing Guidelines\n- 请补充测试框架与推荐命令。\n\n## Security & Configuration Tips\n- 不要提交密钥、Cookie、日志或本地配置。\n\n## workflows\n**Workflow Rules（规范化）**\n- 每轮结束前，更新 `docs/task/progress.md`。\n- 提交前确保 `docs/task/progress.md` 已更新并纳入提交。\n- 合并/提交前必须读取 `git status` 与相关 diff。\n- `src/` 新目录/新入口变更需同步更新 module map。\n- 每次会话结束后，如有必要补全 spec 架构与文档入口。\n- 当用户说 `continue`，直接从 `docs/task/progress.md` 的下一步动作开始执行。\n\n## 附加文档\n- `docs/README.md`\n- `docs/task/progress.md`\n- `docs/sprint/README.md`\n- `docs/spec/README.md`\n""",
    "CLAUDE.md": """# CLAUDE\n\nSee AGENTS.md for repository rules, workflows, and AI constraints.\n""",
    "docs/README.md": """# Docs Index\n\n## Reading Order\n1. docs/task/progress.md - 当前活跃热点\n2. docs/qa/pitfalls.md - 编码前避坑索引\n3. docs/sprint/README.md - Sprint 索引\n4. docs/spec/README.md - 合同索引\n\n## Core\n- docs/rules/PROJECT_RULES.md\n- docs/review/ai-workflow.md\n- docs/task/progress.md\n- docs/sprint/README.md\n\n## QA\n- docs/qa/pitfalls.md - 活跃坑位\n- docs/qa/pitfalls_archive/ - 完整 RCA 归档\n- docs/qa/tests_guideline.txt - 测试规范\n\n## Specs\n- docs/spec/README.md\n\n## Research\n- docs/research/README.md\n\n## Design\n- docs/design/README.md\n\n## Module Maps\n{module_maps}\n""",
    "docs/task/progress.md": """# 任务进展记录\n\n更新时间：{date}\n\n## 当前热点\n- 待补充\n\n## Next Action\n- 待补充\n\n## 今日进展\n- 初始化 spec 架构\n\n## 明日计划\n- 待补充\n\n## 风险与阻塞\n- 待补充\n\n## 关联链接\n- README.md\n- docs/README.md\n""",
    "docs/sprint/README.md": """# Sprint Index\n\n{sprint_files}\n""",
    "docs/spec/README.md": """# Specs Index\n\nSpecs are historical references unless explicitly marked active.\n""",
    "docs/design/README.md": """# Design Notes\n\nPlace architecture notes, diagrams, and state models here.\n""",
    "docs/rules/PROJECT_RULES.md": """# 项目开发规则 (Project Development Rules)\n\n请在此补充本项目的强约束与规则。\n""",
    "docs/review/ai-workflow.md": """# AI 工作流程\n\n请在此补充本项目的 AI 工作流程规范。\n""",
    "docs/qa/tests_guideline.txt": """测试规范 (Testing Guidelines)\n\n请在此补充测试规范与推荐命令。\n""",
    "docs/qa/pitfalls.md": PITFALLS_TEMPLATE,
    "docs/qa/pitfalls_archive/README.md": PITFALLS_ARCHIVE_README,
    "docs/task/archive/.gitkeep": "",
    "docs/research/README.md": """# Research Index\n\nPlace research notes, evidence, and experiment logs here.\n""",
}

TEMPLATE_OVERRIDES = {
    "AGENTS.md": "AGENTS.md",
    "docs/rules/PROJECT_RULES.md": "PROJECT_RULES.md",
    "docs/review/ai-workflow.md": "ai-workflow.md",
    "docs/qa/tests_guideline.txt": "tests_guideline.txt",
}

RAW_TEMPLATE_KEYS = {
    "docs/rules/PROJECT_RULES.md",
    "docs/review/ai-workflow.md",
    "docs/qa/tests_guideline.txt",
    "docs/qa/pitfalls.md",
    "docs/qa/pitfalls_archive/README.md",
    "docs/task/archive/.gitkeep",
}

MODULE_MAP_TEMPLATE = """# Module Map: {module_path}\n\nPurpose\n- TBD\n\nInputs\n- TBD\n\nOutputs\n- TBD\n\nEntry Points\n{entrypoints}\n\nConstraints\n- TBD\n"""


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, content, overwrite=False):
    existed = os.path.exists(path)
    if existed and not overwrite:
        return "skipped"
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return "updated" if existed else "created"


def apply_template_overrides():
    for key, filename in TEMPLATE_OVERRIDES.items():
        path = os.path.join(SKILL_DIR, "templates", filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                TEMPLATES[key] = f.read()


def render_template(rel, template, context):
    if rel in RAW_TEMPLATE_KEYS:
        return template
    return template.format(**context)


def _glob_in_root(root, pattern):
    results = []
    if "*" not in pattern:
        candidate = os.path.join(root, pattern)
        if os.path.exists(candidate):
            results.append(pattern)
        return results
    for name in os.listdir(root):
        if fnmatch.fnmatch(name, pattern):
            results.append(name)
    return results


def detect_languages(root):
    languages = []
    manifests = []
    for lang, patterns in LANGUAGE_FILES.items():
        for pattern in patterns:
            hits = _glob_in_root(root, pattern)
            if hits:
                languages.append(lang)
                manifests.extend(hits)
                break
    return sorted(set(languages)), sorted(set(manifests))


def detect_entrypoints(root):
    entrypoints = []
    for rel in ENTRYPOINT_CANDIDATES:
        if os.path.exists(os.path.join(root, rel)):
            entrypoints.append(rel)
    return entrypoints


def parse_package_json(root):
    path = os.path.join(root, "package.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def detect_project_name(root, default_name):
    pyproject = os.path.join(root, "pyproject.toml")
    if os.path.exists(pyproject):
        try:
            text = open(pyproject, "r", encoding="utf-8").read()
            match = re.search(r"\bname\s*=\s*\"([^\"]+)\"", text)
            if match:
                return match.group(1)
        except Exception:
            pass

    cargo = os.path.join(root, "Cargo.toml")
    if os.path.exists(cargo):
        try:
            text = open(cargo, "r", encoding="utf-8").read()
            match = re.search(r"\bname\s*=\s*\"([^\"]+)\"", text)
            if match:
                return match.group(1)
        except Exception:
            pass

    go_mod = os.path.join(root, "go.mod")
    if os.path.exists(go_mod):
        try:
            text = open(go_mod, "r", encoding="utf-8").read()
            match = re.search(r"^module\s+(.+)$", text, flags=re.MULTILINE)
            if match:
                return match.group(1).strip()
        except Exception:
            pass

    pkg = parse_package_json(root)
    if pkg.get("name"):
        return str(pkg["name"])

    return default_name


def format_list(items, empty="TBD"):
    return ", ".join(items) if items else empty


def has_pytest(root):
    for name in ("requirements.txt", "pyproject.toml"):
        path = os.path.join(root, name)
        if not os.path.exists(path):
            continue
        try:
            text = open(path, "r", encoding="utf-8").read().lower()
        except Exception:
            continue
        if "pytest" in text:
            return True
    return False


def build_quickstart(languages, entrypoints, pkg_json):
    lines_cn = []
    lines_en = []
    entry = entrypoints[0] if entrypoints else None

    if "Python" in languages:
        lines_cn.append("- Python: `python3 -m venv myvenv && source myvenv/bin/activate`")
        if entry:
            lines_cn.append(f"- Python: `python {entry}`")
        lines_en.append("- Python: `python3 -m venv myvenv && source myvenv/bin/activate`")
        if entry:
            lines_en.append(f"- Python: `python {entry}`")

    if "Node" in languages:
        scripts = pkg_json.get("scripts", {}) if isinstance(pkg_json, dict) else {}
        if "start" in scripts:
            lines_cn.append("- Node: `npm install && npm run start`")
            lines_en.append("- Node: `npm install && npm run start`")
        elif entry:
            lines_cn.append(f"- Node: `node {entry}`")
            lines_en.append(f"- Node: `node {entry}`")
        else:
            lines_cn.append("- Node: `npm install` 后补充启动命令")
            lines_en.append("- Node: run `npm install`, then add start command")

    if "Go" in languages:
        lines_cn.append("- Go: `go run ./...`")
        lines_en.append("- Go: `go run ./...`")

    if "Rust" in languages:
        lines_cn.append("- Rust: `cargo run`")
        lines_en.append("- Rust: `cargo run`")

    if "Java" in languages:
        lines_cn.append("- Java: `mvn -q test` 或 `gradle test`")
        lines_en.append("- Java: `mvn -q test` or `gradle test`")

    if ".NET" in languages:
        lines_cn.append("- .NET: `dotnet run`")
        lines_en.append("- .NET: `dotnet run`")

    if "Ruby" in languages:
        lines_cn.append("- Ruby: `bundle exec ruby <entry>` 或 `bundle exec rspec`")
        lines_en.append("- Ruby: `bundle exec ruby <entry>` or `bundle exec rspec`")

    if "PHP" in languages:
        lines_cn.append("- PHP: `composer install` 后补充入口")
        lines_en.append("- PHP: run `composer install`, then add entry")

    if "Swift" in languages:
        lines_cn.append("- Swift: `swift run`")
        lines_en.append("- Swift: `swift run`")

    if not lines_cn:
        lines_cn.append("- 待补充")
    if not lines_en:
        lines_en.append("- TBD")

    return "\n".join(lines_cn), "\n".join(lines_en)


def build_test_commands(languages, pkg_json, root):
    lines_cn = []
    lines_en = []

    if "Python" in languages:
        if has_pytest(root):
            lines_cn.append("pytest")
            lines_en.append("pytest")
        else:
            lines_cn.append("pytest (如已配置)")
            lines_en.append("pytest (if configured)")

    if "Node" in languages:
        scripts = pkg_json.get("scripts", {}) if isinstance(pkg_json, dict) else {}
        if "test" in scripts:
            lines_cn.append("npm test")
            lines_en.append("npm test")
        else:
            lines_cn.append("npm run test (如已配置)")
            lines_en.append("npm run test (if configured)")

    if "Go" in languages:
        lines_cn.append("go test ./...")
        lines_en.append("go test ./...")

    if "Rust" in languages:
        lines_cn.append("cargo test")
        lines_en.append("cargo test")

    if "Java" in languages:
        lines_cn.append("mvn -q test 或 gradle test")
        lines_en.append("mvn -q test or gradle test")

    if ".NET" in languages:
        lines_cn.append("dotnet test")
        lines_en.append("dotnet test")

    if "Ruby" in languages:
        lines_cn.append("bundle exec rspec")
        lines_en.append("bundle exec rspec")

    if "PHP" in languages:
        lines_cn.append("composer test 或 phpunit")
        lines_en.append("composer test or phpunit")

    if "Swift" in languages:
        lines_cn.append("swift test")
        lines_en.append("swift test")

    if not lines_cn:
        lines_cn.append("待补充")
    if not lines_en:
        lines_en.append("TBD")

    return " / ".join(lines_cn), " / ".join(lines_en)


def find_module_entrypoints(module_dir):
    exts = (".py", ".ts", ".js", ".go", ".rs", ".java", ".cs", ".rb", ".php", ".swift")
    entrypoints = []
    try:
        for name in os.listdir(module_dir):
            if name.endswith(exts) and not name.startswith("_"):
                entrypoints.append(name)
    except FileNotFoundError:
        return []
    return entrypoints[:5]


def render_module_maps(root):
    lines = []
    for module_dir in DEFAULT_MODULE_DIRS:
        abs_dir = os.path.join(root, module_dir)
        if not os.path.isdir(abs_dir):
            continue
        lines.append(f"- {module_dir}/README.md")
    return "\n".join(lines) if lines else "- TBD"


def detect_sprint_files(root):
    sprint_dir = os.path.join(root, "docs", "sprint")
    if not os.path.isdir(sprint_dir):
        return []
    names = []
    for name in sorted(os.listdir(sprint_dir)):
        if name.startswith("sprint") and name.endswith(".md"):
            names.append(f"docs/sprint/{name}")
    return names


def main():
    parser = argparse.ArgumentParser(description="Spec architecture audit/bootstrap")
    parser.add_argument("--root", default=os.getcwd(), help="repo root")
    parser.add_argument("--mode", choices=["audit", "write"], default="write")
    parser.add_argument("--profile", choices=["minimal", "full"], default="full")
    parser.add_argument("--update-existing", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    project_name = os.path.basename(root.rstrip(os.sep)) or "Project"
    date = datetime.now().strftime("%Y-%m-%d")

    apply_template_overrides()

    languages, manifests = detect_languages(root)
    entrypoints = detect_entrypoints(root)
    pkg_json = parse_package_json(root)
    project_name = detect_project_name(root, project_name)
    quick_start_cn, quick_start_en = build_quickstart(languages, entrypoints, pkg_json)
    test_cn, test_en = build_test_commands(languages, pkg_json, root)
    module_maps = render_module_maps(root)

    sprint_files = detect_sprint_files(root)
    sprint_block = "\n".join(f"- {name}" for name in sprint_files) if sprint_files else "- docs/sprint/sprint1.md"

    required = [
        "README.md",
        "README.en.md",
        "AGENTS.md",
        "CLAUDE.md",
        "docs/README.md",
        "docs/task/progress.md",
        "docs/sprint/README.md",
        "docs/spec/README.md",
        "docs/design/README.md",
    ]

    if args.profile == "full":
        required.extend([
            "docs/rules/PROJECT_RULES.md",
            "docs/review/ai-workflow.md",
            "docs/qa/tests_guideline.txt",
            "docs/qa/pitfalls.md",
            "docs/qa/pitfalls_archive/README.md",
            "docs/task/archive/.gitkeep",
            "docs/research/README.md",
        ])

    created = []
    skipped = []
    missing = []

    context = {
        "project_name": project_name,
        "date": date,
        "languages": format_list(languages),
        "entrypoints": format_list(entrypoints),
        "manifests": format_list(manifests),
        "quick_start_cn": quick_start_cn,
        "quick_start_en": quick_start_en,
        "test_commands": format_list([test_cn]),
        "module_maps": module_maps,
        "sprint_files": sprint_block,
    }

    for rel in required:
        path = os.path.join(root, rel)
        exists = os.path.exists(path)
        if exists and not args.update_existing:
            skipped.append(rel)
            continue
        if not exists:
            missing.append(rel)
        if args.mode == "write":
            template = TEMPLATES.get(rel)
            if template is None:
                continue
            content = render_template(rel, template, context)
            result = write_file(path, content, overwrite=args.update_existing)
            if result in ("created", "updated"):
                created.append(rel)

    module_maps_result = []
    for module_dir in DEFAULT_MODULE_DIRS:
        abs_dir = os.path.join(root, module_dir)
        if not os.path.isdir(abs_dir):
            continue
        map_rel = os.path.join(module_dir, "README.md")
        map_path = os.path.join(root, map_rel)
        if os.path.exists(map_path):
            module_maps_result.append({"path": map_rel, "status": "exists"})
            continue
        if args.mode == "write":
            entry_list = find_module_entrypoints(abs_dir)
            entry_text = "- " + "\n- ".join(entry_list) if entry_list else "- TBD"
            content = MODULE_MAP_TEMPLATE.format(module_path=module_dir, entrypoints=entry_text)
            write_file(map_path, content, overwrite=args.update_existing)
            module_maps_result.append({"path": map_rel, "status": "created"})
        else:
            module_maps_result.append({"path": map_rel, "status": "missing"})

    summary = {
        "root": root,
        "mode": args.mode,
        "profile": args.profile,
        "missing": missing,
        "created": created,
        "skipped": skipped,
        "module_maps": module_maps_result,
    }

    if args.print_json:
        print(json.dumps(summary, ensure_ascii=True, indent=2))
    else:
        print("Spec architecture summary")
        print(f"root: {root}")
        print(f"mode: {args.mode}")
        print(f"profile: {args.profile}")
        print(f"missing: {len(missing)}")
        print(f"created: {len(created)}")
        print(f"module_maps: {len(module_maps_result)}")


if __name__ == "__main__":
    main()
