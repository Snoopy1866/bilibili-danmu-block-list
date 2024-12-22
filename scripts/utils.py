def render_markdown(rules: list[dict[str, str]]) -> str:
    markdown = ""
    for rule in rules:
        filter = rule["filter"]
        type = rule["type"]
        opened = rule["opened"]
        examples = rule.get("examples", "")

        filter_markdown = "`" + filter.replace("|", "\\|") + "`"
        if type == 0:
            type_markdown = "文本"
        elif type == 1:
            type_markdown = "正则"
        elif type == 2:
            type_markdown = "用户"
        else:
            raise ValueError(f"Unknown type: {type}")
        if opened:
            opened_markdown = "是"
        else:
            opened_markdown = "否"
        examples_markdown = "\n".join([f"    - {example}" for example in examples])

        markdown += f"- {filter_markdown}\n"
        markdown += f"  - 类型：{type_markdown}\n"
        markdown += f"  - 是否启用：{opened_markdown}\n"
        markdown += f"  - 示例：\n{examples_markdown}\n"
    return markdown
