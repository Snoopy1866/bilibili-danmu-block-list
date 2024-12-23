from __future__ import annotations

from enum import Enum


class RuleType(Enum):
    TEXT = 0
    REGEX = 1
    USER = 2

    def __str__(self) -> str:
        if self == RuleType.TEXT:
            return "文本"
        elif self == RuleType.REGEX:
            return "正则"
        elif self == RuleType.USER:
            return "用户"
        else:
            assert False, f"Unknown type: {self}"


class Rule:
    def __init__(
        self,
        type: RuleType,
        filter: str,
        opened: bool,
        id: int,
        description: str,
        examples: list[str],
        exclude_examples: list[str],
    ):
        self.type = type
        self.filter = filter
        self.opened = opened
        self.id = id
        self.description = description
        self.examples = examples
        self.exclude_examples = exclude_examples

    @classmethod
    def from_dict(cls, dict: dict) -> Rule:
        try:
            type = RuleType(dict.get("type"))
            filter = dict.get("filter")
            opened = dict.get("opened")
            id = dict.get("id", -1)
            description = dict.get("description", "")
            examples = dict.get("examples", [])
            exclude_examples = dict.get("exclude_examples", [])
        except Exception as e:
            raise ValueError(f"Invalid rule: {dict}") from e
        else:
            return cls(
                type=type,
                filter=filter,
                opened=opened,
                id=id,
                description=description,
                examples=examples,
                exclude_examples=exclude_examples,
            )

    def to_dict(self, verbose: bool = False) -> dict:
        if verbose:
            return {
                "type": self.type.value,
                "filter": self.filter,
                "opened": self.opened,
                "id": self.id,
                "description": self.description,
                "examples": self.examples,
                "exclude_examples": self.exclude_examples,
            }
        else:
            return {
                "type": self.type.value,
                "filter": self.filter,
                "opened": self.opened,
                "id": self.id,
            }

    def to_markdown_ul(self) -> str:
        type_markdown = str(self.type)
        filter_markdown = f"`{self.filter}`"
        opened_markdown = "是" if self.opened else "否"

        if self.examples:
            examples_markdown = "\n".join([f"    - `{example}`" for example in self.examples])
        else:
            examples_markdown = "    无"

        if self.exclude_examples:
            exclude_examples_markdown = "\n".join([f"    - `{example}`" for example in self.exclude_examples])
        else:
            exclude_examples_markdown = "    无"

        markdown = (
            f"- {filter_markdown}\n"
            + f"  - 类型：{type_markdown}\n"
            + f"  - 是否启用：{opened_markdown}\n"
            + f"  - 匹配示例：\n{examples_markdown}\n"
            + f"  - 排除示例：\n{exclude_examples_markdown}\n"
        )
        return markdown

    def to_markdown_tr(self, verbose: bool = False) -> str:
        type_markdown = str(self.type)
        filter_markdown = f"`{self.filter}`"
        opened_markdown = "是" if self.opened else "否"

        if self.examples:
            examples_markdown = "、".join([f"`{example}`" for example in self.examples])
        else:
            examples_markdown = "/"

        if self.exclude_examples:
            exclude_examples_markdown = "、".join([f"`{example}`" for example in self.exclude_examples])
        else:
            exclude_examples_markdown = "/"

        if verbose:
            markdown = f"| {filter_markdown} | {type_markdown} | {opened_markdown} | {examples_markdown} | {exclude_examples_markdown} |"
        else:
            markdown = f"| {filter_markdown} | {examples_markdown} |"
        return markdown