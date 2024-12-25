import json
from collections import Counter
import re
from jsonschema import validate

from const import BILIBILI_BLOCK_SCHEMA, BILIBILI_BLOCK
from utils import Rule, RuleType


def check_duplicate_filters(rules: list[Rule]) -> None:
    """检查是否有过滤器重复的规则

    Args:
        rules (list[Rule]): 规则列表

    Raises:
        ValueError: 存在过滤器重复的规则
    """
    filters = [rule.filter for rule in rules]
    duplicated_filters = [filter for filter, count in Counter(filters).items() if count > 1]
    duplicated_rules = [rule for rule in rules if rule.filter in duplicated_filters]
    if duplicated_filters:
        raise ValueError(
            f"存在过滤器重复的规则:\n{"\n".join([str(duplicated_rule) for duplicated_rule in duplicated_rules])}"
        )


def check_duplicate_ids(rules: list[Rule]) -> None:
    """检查是否有 ID 重复的规则

    Args:
        rules (list[Rule]): 规则列表

    Raises:
        ValueError: 存在 ID 重复的规则
    """
    ids = [rule.id for rule in rules]
    duplicated_ids = [id for id, count in Counter(ids).items() if count > 1]
    duplicated_rules = [rule for rule in rules if rule.id in duplicated_ids]
    if duplicated_ids:
        raise ValueError(
            f"存在 ID 重复的规则:\n{"\n".join([str(duplicated_rule) for duplicated_rule in duplicated_rules])}"
        )


def check_rule_of_user(rules: list[Rule]) -> None:
    """检查是否有屏蔽用户的规则

    Args:
        rules (list[Rule]): 规则列表

    Raises:
        ValueError: 存在屏蔽用户的规则
    """
    block_user_rules = [rule for rule in rules if rule.type == RuleType.USER]
    if block_user_rules:
        raise ValueError(
            f"存在屏蔽用户的规则:\n{"\n".join([str(block_user_rule) for block_user_rule in block_user_rules])}"
        )


def check_regex(rules: list[Rule]) -> None:
    """检查正则表达式是否匹配

    Args:
        rules (list[Rule]): 规则列表

    Raises:
        ValueError: 正则表达式未能匹配需屏蔽的字符串
        ValueError: 正则表达式错误匹配需排除的字符串
    """
    for rule in rules:
        if rule.type == RuleType.REGEX:
            try:
                pattern = re.compile(rule.filter)
                for example in rule.examples:
                    if not pattern.search(example):
                        raise ValueError(f"正则表达式未能匹配需屏蔽的字符串: '{example}'")
                for example in rule.exclude_examples:
                    if pattern.search(example):
                        raise ValueError(f"正则表达式错误匹配需排除的字符串: '{example}'")
            except ValueError as e:
                raise ValueError(f"规则 {rule} 错误: {e}") from e


def main() -> None:
    try:
        with open(BILIBILI_BLOCK_SCHEMA, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
            instance = json.load(f)

        validate(instance, schema)

        rules = [Rule.from_dict(rule) for rule in instance["rules"]]

        check_duplicate_filters(rules)

        check_duplicate_ids(rules)

        check_rule_of_user(rules)

        check_regex(rules)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
