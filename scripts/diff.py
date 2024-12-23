import json

from utils import Rule

OLD_JSON = "bilibili-danmu-blocklist-old.json"
NEW_JSON = "bilibili-danmu-blocklist.json"
DIFF_MARKDOWN = "diff.md"


def get_diff_rules(old_json: str, new_json: str) -> tuple[list[Rule], list[Rule]]:
    """获取新增和移除的规则

    Args:
        old_json (str): 旧版本的 JSON 文件
        new_json (str): 新版本的 JSON 文件

    Returns:
        tuple[list[Rule], list[Rule]]: 新增的规则和移除的规则
    """
    with open(old_json, "r", encoding="utf-8") as f:
        old_data = json.load(f)
    with open(new_json, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    old_rules: list[Rule] = [Rule.from_dict(rule) for rule in old_data["rules"]]
    new_rules: list[Rule] = [Rule.from_dict(rule) for rule in new_data["rules"]]

    old_filters = set(rule.filter for rule in old_rules)
    new_filters = set(rule.filter for rule in new_rules)
    added_filters = new_filters - old_filters
    removed_filters = old_filters - new_filters

    added_rules = [rule for rule in new_rules if rule.filter in added_filters]
    removed_rules = [rule for rule in old_rules if rule.filter in removed_filters]

    return added_rules, removed_rules


def main() -> None:
    try:
        added_rules, removed_rules = get_diff_rules(OLD_JSON, NEW_JSON)

        with open(DIFF_MARKDOWN, "w", encoding="utf-8") as f:
            f.write("## 新增规则\n")
            f.write("|规则|示例|\n")
            f.write("|----|----|\n")
            for rule in added_rules:
                f.write(rule.to_markdown_tr())

            f.write("\n")

            f.write("## 移除规则\n")
            f.write("|规则|示例|\n")
            f.write("|----|----|\n")
            for rule in removed_rules:
                f.write(rule.to_markdown_tr())
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
