# -*- encoding: utf-8 -*-
"""基础文件"""

import re
import json
import sys
import tomllib as tl
from pathlib import Path
from typing import Dict, List, Tuple, TypeAlias

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
    "advancements": config["category"]["ignore_advancements"],
    "biome": config["category"]["ignore_biome"],
    "block": config["category"]["ignore_block"],
    "entity": config["category"]["ignore_entity"],
    "item": config["category"]["ignore_item"],
    "effect": config["category"]["ignore_effect"],
    "enchantment": config["category"]["ignore_enchantment"],
}
IGNORE_SAVED_IMAGE = config["image"]["ignore_saved_image"]
IGNORE_SUPPLEMENTS = config["lang"]["ignore_supplements"]
NEW_STRINGS_ONLY = config["lang"]["new_strings_only"]


def is_valid_key(input_key: str, *categories: str) -> bool:
    """
    判断是否为有效键名。

    Args:
        input_key (str): 键名
        categories (str): 多个类别（如 'block', 'entity', 'item'）

    Returns:
        bool: 如果是有效键名，返回 True，否则返回 False
    """
    return any(input_key.startswith(f"{category}") for category in categories)


# 读取语言文件
if NEW_STRINGS_ONLY:
    LANG_FILE_PATH = P / "en_us_diff.json"
else:
    LANG_FILE_PATH = LANG_DIR / "en_us.json"
if not LANG_FILE_PATH.exists():
    print("\n无法找到语言文件，请检查文件路径。")
    sys.exit()
with open(LANG_FILE_PATH, "r", encoding="utf-8") as f:
    language_data: Ldata = json.load(f)

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


update_data = {
    "item.minecraft.netherite_upgrade_smithing_template": "Netherite Upgrade Smithing Template",
    "item.minecraft.music_disc_*": "Music Disc",
    "item.minecraft.*_banner_pattern": "Banner Pattern",
}

if not NEW_STRINGS_ONLY:
    language_data.update(update_data)
