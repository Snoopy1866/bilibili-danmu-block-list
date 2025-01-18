import json

from const import BILIBILI_BLOCK
from utils import Rule


def main():
    try:
        with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
            data: dict = json.load(f)

        rules: list[Rule] = [Rule.from_dict(rule) for rule in data["rules"]]
        rules_markdown: list[str] = [rule.to_markdown_ul() for rule in rules]

        with open("rules.md", "w", encoding="utf-8") as f:
            f.write("# bilibili 弹幕屏蔽规则清单\n")
            f.write("\n")
            for rule_markdown in rules_markdown:
                f.write(rule_markdown)
                f.write("\n")
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
