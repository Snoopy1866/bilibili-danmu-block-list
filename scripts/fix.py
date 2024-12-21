import json
from pypinyin import lazy_pinyin

from const import BILIBILI_BLOCK


def sort() -> None:
    with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
        data = json.load(f)

    rules: list[dict] = data["rules"]
    rules.sort(key=lambda rule: lazy_pinyin(rule["filter"]))

    with open(BILIBILI_BLOCK, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    try:
        sort()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
