# -*- encoding: utf-8 -*-
"""基础文件"""

import re
import json
import sys
import tomllib as tl
from pathlib import Path

# 当前绝对路径
P = Path(__file__).resolve().parent

# 加载配置
CONFIG_DIR = P / "configuration.toml"
if not CONFIG_DIR.exists():
    print("\n无法找到配置文件，请将配置文件放置在与此脚本同级的目录下。")
    sys.exit()
with open(CONFIG_DIR, "rb") as f:
    config = tl.load(f)

# 读取配置
LANG_DIR = P / config["folder"]["language_folder"]
IMAGE_DIR = P / config["folder"]["image_folder"]
LOG_DIR = P / config["folder"]["log_folder"]
PPT_DIR = P / config["folder"]["slide_folder"]
SLIDE_CONFIG = config["slide"]
IGNORE_BLOCK = config["category"]["ignore_block"]
IGNORE_ENTITY = config["category"]["ignore_entity"]
IGNORE_ITEM = config["category"]["ignore_item"]
IGNORE_EFFECT = config["category"]["ignore_effect"]
IGNORE_ENCHANTMENT = config["category"]["ignore_enchantment"]
IGNORE_SAVED_IMAGE = config["image"]["ignore_saved_image"]


def is_valid_block(block_key: str):
    """判断是否为有效方块键名"""
    if (
        block_key.startswith("block.")
        and not re.match(r"block\.minecraft\.(.*)\.", block_key)
        and block_key != "block.minecraft.set_spawn"
    ):
        return True
    return False


def is_valid_entity(entity_key: str):
    """判断是否为有效实体键名"""
    if (
        entity_key.startswith("entity.minecraft.")
        and not re.match(r"entity\.minecraft\.(.*)\.", entity_key)
        and entity_key != "entity.minecraft.falling_block_type"
    ):
        return True
    return False


def is_valid_item(item_key: str):
    """判断是否为有效物品键名"""
    if (
        item_key.startswith("item.minecraft.")
        and not re.match(r"item\.minecraft\.(.*)\.", item_key)
        and "pottery_shard" not in item_key
    ) or re.match(r"item\.minecraft\.(.*)\.effect", item_key):
        return True
    return False


# 读取语言文件
with open(LANG_DIR / "en_us.json", "r", encoding="utf-8") as f:
    language_data = json.load(f)

# 修正语言文件
keys_to_remove = [
    key
    for key in language_data.keys()
    if key.startswith("item.minecraft.music_disc")
    or re.match(r"item\.minecraft\.(.*)_banner_pattern", key)
]
for key in keys_to_remove:
    del language_data[key]
del language_data["item.minecraft.smithing_template"]

updated_language_data = language_data

for key, value in language_data.items():
    if "trim_smithing_template" in key:
        variant = key.split(".")[2].split("_", maxsplit=1)[0]
        updated_language_data[
            key
        ] = f"{updated_language_data[f'trim_pattern.minecraft.{variant}']} Smithing Template"

language_data = updated_language_data

language_data.update(
    {
        "item.minecraft.netherite_upgrade_smithing_template": "Netherite Upgrade Smithing Template",
        "item.minecraft.music_disc_*": "Music Disc",
        "item.minecraft.*_banner_pattern": "Banner Pattern",
    }
)
