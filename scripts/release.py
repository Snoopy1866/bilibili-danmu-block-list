import json

from const import BILIBILI_BLOCK, BILIBILI_BLOCK_RELEASE_OUTPUT


def extract_rules() -> None:
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


def main() -> None:
    try:
        extract_rules()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
