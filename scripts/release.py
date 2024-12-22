import json

from const import BILIBILI_BLOCK, BILIBILI_BLOCK_RELEASE_OUTPUT
from json2md import render_markdown


def make_json() -> None:
    with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
        data = json.load(f)

    rules = data["rules"]
    rules = [
        {
            "type": rule["type"],
            "filter": rule["filter"],
            "opened": rule["opened"],
        }
        for rule in rules
    ]

    with open(BILIBILI_BLOCK_RELEASE_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False)


def make_markdown() -> None:
    with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
        data = json.load(f)
    rules = data["rules"]
    rules_markdown = render_markdown(rules)

    with open("rules.md", "w", encoding="utf-8") as f:
        f.write("# bilibili 弹幕屏蔽规则清单\n")
        f.write(rules_markdown)


def main() -> None:
    try:
        make_json()
        make_markdown()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
