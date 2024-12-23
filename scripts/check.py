import json
from collections import Counter
from jsonschema import validate

from const import BILIBILI_BLOCK_SCHEMA, BILIBILI_BLOCK
from utils import Rule, RuleType


def validate_bilibili_block_json() -> None:
    with open(BILIBILI_BLOCK_SCHEMA, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(BILIBILI_BLOCK, "r", encoding="utf-8") as f:
        instance = json.load(f)

    rules = instance["rules"]

    # 验证是否符合 bilibili-block-schema.json 定义的规范
    validate(instance, schema)

    # 转化为 Rule 对象
    rules = [Rule.from_dict(rule) for rule in rules]

    # 验证是否有重复的规则
    filters = [rule.filter for rule in rules]
    duplicated_filters = [
        filter for filter, count in Counter(filters).items() if count > 1
    ]
    if duplicated_filters:
        raise ValueError(f"重复的规则: {duplicated_filters}")

    # 验证是否有屏蔽用户的规则
    blocked_users = [rule.filter for rule in rules if rule.type == RuleType.USER]
    if blocked_users:
        raise ValueError(f"存在屏蔽用户的规则: {blocked_users}")


def main() -> None:
    try:
        validate_bilibili_block_json()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
