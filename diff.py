# -*- encoding: utf-8 -*-
"""检查新增字符串"""

import json
import re
from typing import Tuple, Dict, Set
from base import P, LANG_DIR

# 定义常量
PREFIXES: Tuple[str, ...] = (
    "block.",
    "item.minecraft.",
    "entity.minecraft.",
    "biome.",
    "effect.minecraft.",
    "enchantment.minecraft.",
    "trim_pattern.",
    "upgrade.",
    "filled_map",
)
INVALID_BLOCK_ITEM_ENTITY_PATTERN = re.compile(
    r"(block\.minecraft\.|item\.minecraft\.|entity\.minecraft\.)[^.]*\."
)
ITEM_EFFECT_PATTERN = re.compile(r"item\.minecraft\.[^.]*\.effect\.[^.]*")
ADVANCEMENTS_TITLE_PATTERN = re.compile(r"advancements\.(.*)\.title")
EXCLUSIONS: Set[str] = {
    "block.minecraft.set_spawn",
    "entity.minecraft.falling_block_type",
    "filled_map.id",
    "filled_map.level",
    "filled_map.locked",
    "filled_map.scale",
    "filled_map.unknown",
}


def is_valid_key(translation_key: str) -> bool:
    """
    判断是否为有效键名。

    Args:
        translation_key (str): 需要验证的键名

    Returns:
        bool: 如果键名有效，返回 True；否则返回 False
    """

    if ADVANCEMENTS_TITLE_PATTERN.match(translation_key):
        return True
    if not translation_key.startswith(PREFIXES):
        return False
    if translation_key in EXCLUSIONS or "pottery_shard" in translation_key:
        return False
    if ITEM_EFFECT_PATTERN.match(translation_key):
        return True
    if INVALID_BLOCK_ITEM_ENTITY_PATTERN.match(translation_key):
        return False
    return True


# 修改语言文件
with open(P / "en_us.json", "r", encoding="utf-8") as l:
    data_old: Dict[str, str] = json.load(l)
edited_data: Dict[str, str] = {k: v for k, v in data_old.items() if is_valid_key(k)}
print("已提取旧“en_us.json”的有效字符串。")

with open(LANG_DIR / "en_us.json", "r", encoding="utf-8") as l:
    data_new: Dict[str, str] = json.load(l)

diff_data = {k: v for k, v in data_new.items() if k not in data_old}

with open(P / "en_us_diff.json", "w", encoding="utf-8") as l:
    json.dump(diff_data, l, ensure_ascii=False, indent=4)
print("已提取“en_us.json”中新增的字符串。")
