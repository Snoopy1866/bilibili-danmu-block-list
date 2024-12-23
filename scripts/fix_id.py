import json

from const import BILIBILI_BLOCK
from utils import Rule


def set_id() -> None:
    """设置规则 ID"""
    with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
        data = json.load(f)

    rules: list[dict] = data["rules"]

    _obj: list[Rule] = [Rule.from_dict(rule) for rule in rules]

    _dict: list[dict] = [obj.to_dict(verbose=True) for obj in _obj]

    data["rules"] = _dict

    with open(BILIBILI_BLOCK, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    try:
        set_id()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
