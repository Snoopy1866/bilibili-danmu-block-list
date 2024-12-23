import json

from const import BILIBILI_BLOCK
from utils import Rule

BILIBILI_BLOCK_RELEASE_OUTPUT = "bilibili-danmu-blocklist-output.json"


def main() -> None:
    try:
        with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
        rules: list[Rule] = [Rule.from_dict(rule) for rule in data["rules"]]

        rules_simplified = [rule.to_dict() for rule in rules]

        with open(BILIBILI_BLOCK_RELEASE_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(rules_simplified, f, ensure_ascii=False)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
