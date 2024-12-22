import json

from const import BILIBILI_BLOCK


def render_markdown(rules: list[dict[str, str]]) -> str:
    markdown = ""
    for rule in rules:
        filter = rule["filter"]
        type = rule["type"]
        opened = rule["opened"]
        examples = rule.get("examples", "")

        filter_markdown = f"`{filter}`"
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

        if examples:
            examples_markdown = "\n".join(
                [f"    - `{example}`" for example in examples]
            )
        else:
            examples_markdown = "无"

        markdown += f"- {filter_markdown}\n"
        markdown += f"  - 类型：{type_markdown}\n"
        markdown += f"  - 是否启用：{opened_markdown}\n"
        markdown += f"  - 示例：\n{examples_markdown}\n"
    return markdown


def main():
    try:
        with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
            data = json.load(f)
        rules = data["rules"]
        rules_markdown = render_markdown(rules)

        with open("rules.md", "w", encoding="utf-8") as f:
            f.write("# bilibili 弹幕屏蔽规则清单\n")
            f.write(rules_markdown)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
