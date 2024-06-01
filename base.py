# -*- encoding: utf-8 -*-
"""基础文件"""

import re
import json
import sys
import tomllib as tl
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional, TypeAlias

# 当前绝对路径
P = Path(__file__).resolve().parent

# 类型别名
Ldata: TypeAlias = Dict[str, str]
LdataTuple: TypeAlias = List[Tuple[str, str]]

# 加载配置
CONFIG_PATH = P / "configuration.toml"
if not CONFIG_PATH.exists():
    print("\n无法找到配置文件，请将配置文件放置在与此脚本同级的目录下。")
    sys.exit()
with open(CONFIG_PATH, "rb") as f:
    config = tl.load(f)

# 读取配置
LANG_DIR = P / config["folder"]["language_folder"]
IMAGE_DIR = P / config["folder"]["image_folder"]
LOG_DIR = P / config["folder"]["log_folder"]
PPT_DIR = P / config["folder"]["slide_folder"]
SLIDE_CONFIG = config["slide"]
IGNORE_CATEGORIES = {
    "block": config["category"]["ignore_block"],
    "entity": config["category"]["ignore_entity"],
    "item": config["category"]["ignore_item"],
    "effect": config["category"]["ignore_effect"],
    "enchantment": config["category"]["ignore_enchantment"],
}
IGNORE_SAVED_IMAGE = config["image"]["ignore_saved_image"]
IGNORE_SUPPLEMENTS = config["lang"]["ignore_supplements"]


def is_valid_key(
    input_key: str,
    category: str,
    invalid_pattern: str,
    exclusions: Optional[Set[str]] = None,
) -> bool:
    """
    判断是否为有效键名

    Args:
        input_key (str): 键名
        category (str): 类别（如 'block', 'entity', 'item'）
        invalid_pattern (str): 正则无效模式
        exclusions (Set[str]): 排除项

    Returns:
        bool: 如果是有效键名，返回 True，否则返回 False
    """

    if not input_key.startswith(f"{category}.minecraft."):
        return False
    if re.match(invalid_pattern, input_key):
        return False
    if exclusions:
        if input_key in exclusions:
            return False
    return True


def is_valid_block(block_key: str) -> bool:
    """
    判断是否为有效方块键名

    Args:
        block_key (str): 方块键名

    Returns:
        bool: 如果是有效方块键名，返回 True，否则返回 False
    """

    return is_valid_key(
        block_key,
        "block",
        r"^block\.minecraft\.(banner\.[^.]+|[^.]+)\.[^.]+$",
        {"block.minecraft.set_spawn"},
    )


def is_valid_entity(entity_key: str) -> bool:
    """
    判断是否为有效实体键名

    Args:
        entity_key (str): 实体键名

    Returns:
        bool: 如果是有效实体键名，返回 True，否则返回 False
    """

    return is_valid_key(
        entity_key,
        "entity",
        r"^entity\.minecraft\.[^.]+\.[^.]+(\.[^.]+)?$",
        {"entity.minecraft.falling_block_type"},
    )


def is_valid_item(item_key: str) -> bool:
    """
    判断是否为有效物品键名

    Args:
        item_key (str): 物品键名

    Returns:
        bool: 如果是有效物品键名，返回 True，否则返回 False
    """

    return is_valid_key(
        item_key, "item", r"^(item\.minecraft\.[^.]+\.[^.]+(\.[^.]+)?|.*pottery_shard.*)$"
    ) or bool(re.match(r"^item\.minecraft\.[^.]*\.effect\.[^.]*$", item_key))


# 读取语言文件
LANG_FILE_PATH = LANG_DIR / "en_us.json"
if not LANG_FILE_PATH.exists():
    print("\n无法找到语言文件，请检查文件路径。")
    sys.exit()
with open(LANG_FILE_PATH, "r", encoding="utf-8") as f:
    language_data: Dict[str, str] = json.load(f)

# 修正语言文件
keys_to_remove = [
    key
    for key in language_data.keys()
    if key.startswith("item.minecraft.music_disc")
    or re.match(r"^item\.minecraft\.[^.]*_banner_pattern$", key)
]
keys_to_remove.append("item.minecraft.smithing_template")

for key in keys_to_remove:
    language_data.pop(key, None)

updated_language_data = language_data.copy()

for key, value in language_data.items():
    if "trim_smithing_template" in key:
        variant = key.split(".")[2].split("_", maxsplit=1)[0]
        variant_string = updated_language_data.get(
            f"trim_pattern.minecraft.{variant}", variant
        )
        updated_language_data[key] = f"{variant_string} Smithing Template"

language_data.update(updated_language_data)

language_data.update(
    {
        "item.minecraft.netherite_upgrade_smithing_template": "Netherite Upgrade Smithing Template",
        "item.minecraft.music_disc_*": "Music Disc",
        "item.minecraft.*_banner_pattern": "Banner Pattern",
    }
)
