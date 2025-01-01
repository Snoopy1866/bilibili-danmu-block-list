import json

from pypinyin import lazy_pinyin

from utils import Rule

OLD_JSON = "bilibili-danmu-blocklist-old.json"
NEW_JSON = "bilibili-danmu-blocklist.json"
DIFF_MARKDOWN = "diff.md"


def get_diff_rule_ids(old_rules: list[Rule], new_rules: list[Rule]) -> tuple[list[int], list[int], list[int]]:
    """获取新增、移除、更新的规则 ID

    Args:
        old_rules (list[Rule]): 旧版本的规则列表
        new_rules (list[Rule]): 新版本的规则列表

    Returns:
        tuple[list[int], list[int], list[int]]: 新增、移除、更新的规则 ID
    """

    old_ids = set(rule.id for rule in old_rules)
    new_ids = set(rule.id for rule in new_rules)
    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids

    same_ids = old_ids & new_ids
    updated_ids = []
    for id in same_ids:
        old_rule = next(rule for rule in old_rules if rule.id == id)
        new_rule = next(rule for rule in new_rules if rule.id == id)
        if old_rule.filter != new_rule.filter:
            updated_ids.append(id)

    return added_ids, removed_ids, updated_ids


def main() -> None:
    try:
        with open(OLD_JSON, "r", encoding="utf-8") as f:
            old_data = json.load(f)
        with open(NEW_JSON, "r", encoding="utf-8") as f:
            new_data = json.load(f)

        old_rules: list[Rule] = [Rule.from_dict(rule) for rule in old_data["rules"]]
        new_rules: list[Rule] = [Rule.from_dict(rule) for rule in new_data["rules"]]

        added_ids, removed_ids, updated_ids = get_diff_rule_ids(old_rules, new_rules)

        added_rules = [rule for rule in new_rules if rule.id in added_ids]
        removed_rules = [rule for rule in old_rules if rule.id in removed_ids]
        updated_rules_old = [rule for rule in old_rules if rule.id in updated_ids]
        updated_rules_new = [rule for rule in new_rules if rule.id in updated_ids]

        added_rules.sort(key=lambda rule: lazy_pinyin(rule.filter))
        removed_rules.sort(key=lambda rule: lazy_pinyin(rule.filter))

        # 先按照 id 排序，zip 后再按照旧规则的 filter 排序
        updated_rules_old.sort(key=lambda rule: rule.id)
        updated_rules_new.sort(key=lambda rule: rule.id)
        updated_rules = list(zip(updated_rules_old, updated_rules_new))
        updated_rules.sort(key=lambda rule: lazy_pinyin(rule[0].filter))

        with open(DIFF_MARKDOWN, "w", encoding="utf-8") as f:
            if added_rules:
                f.write("## 新增规则\n")
                f.write("|规则|示例|\n")
                f.write("|----|----|\n")
                for rule in added_rules:
                    f.write(f"|{rule.filter.to_markdown_td()}|{rule.examples.to_markdown_td()}|" + "\n")

            f.write("\n")

            if updated_rules:
                f.write("## 更新规则\n")
                f.write("|原规则|新规则|示例|\n")
                f.write("|------|------|----|\n")
                for rule in updated_rules:
                    f.write(
                        f"|{rule[0].filter.to_markdown_td()}|{rule[1].filter.to_markdown_td()}|{rule[1].examples.to_markdown_td()}|"
                        + "\n"
                    )

            f.write("\n")

            if removed_rules:
                f.write("## 移除规则\n")
                f.write("|规则|示例|\n")
                f.write("|----|----|\n")
                for rule in removed_rules:
                    f.write(f"|{rule.filter.to_markdown_td()}|{rule.examples.to_markdown_td()}|" + "\n")
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
