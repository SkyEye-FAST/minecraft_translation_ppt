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
LdataCo: TypeAlias = Dict[str, Ldata]
LdataTuple: TypeAlias = List[Tuple[str, str]]

# 加载配置
CONFIG_PATH = P / "configuration.toml"
if not CONFIG_PATH.exists():
    print("\n无法找到配置文件，请将配置文件放置在与此脚本同级的目录下。")
    sys.exit()
with open(CONFIG_PATH, "rb") as conf:
    config = tl.load(conf)

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

lang_list = ["en_us", "zh_cn", "zh_hk", "zh_tw", "lzh"]
lang_file_list = [f"{l}.json" for l in lang_list]
lang_list_table = lang_list[1:]

def is_valid_key(input_key: str, *categories: str) -> bool:
    """
    判断是否为有效键名。

    Args:
        input_key (str): 键名
        categories (str): （多个）分类

    Returns:
        bool: 如果是有效键名，返回 True，否则返回 False
    """
    return any(input_key.startswith(f"{category}") for category in categories)


def load_language_files(file_list: List[str]) -> Tuple[LdataCo, LdataCo]:
    """
    读取语言文件。

    Args:
        file_list (List[str]): 语言文件名列表

    Returns:
        Tuple[LdataCo, LdataCo]: 包含语言数据的字典
    """

    print("开始读取语言文件。")
    data, data_all = {}, {}
    for file in file_list:
        with open(LANG_DIR / file, "r", encoding="utf-8") as lang:
            data_all[l := file.split(".", maxsplit=1)[0]] = json.load(lang)
            if NEW_STRINGS_ONLY:
                data[l] = {k: v for k, v in data_all[l].items() if k in language_data}
    print("语言文件读取成功。")
    return data, data_all


def sort_data(lang_data: LdataCo, *categories: str) -> Dict[str, LdataTuple]:
    """
    排序语言数据。

    Args:
        lang_data (LdataCo): 语言数据
        categories (str): （多个）分类

    Returns:
        Dict[str, LdataTuple]: 排序后的语言数据
    """

    sorted_data = {
        "en_us": sorted(
            (
                (key, value)
                for key, value in lang_data["en_us"].items()
                if is_valid_key(key, *categories)
            ),
            key=lambda x: x[1],
        )
    }
    sorted_keys = [item[0] for item in sorted_data["en_us"]]
    for lang_name in ["zh_cn", "zh_hk", "zh_tw", "lzh"]:
        sorted_data[lang_name] = sorted(
            (
                (key, value)
                for key, value in lang_data[lang_name].items()
                if is_valid_key(key, *categories)
            ),
            key=lambda x: sorted_keys.index(x[0]),
        )
    return sorted_data


# 读取语言文件
with open(LANG_DIR / "en_us.json", "r", encoding="utf-8") as f:
    language_data_all: Ldata = json.load(f)
if NEW_STRINGS_ONLY:
    LANG_FILE_PATH = P / "en_us_diff.json"
    with LANG_FILE_PATH.open("r", encoding="utf-8") as f:
        language_data: Ldata = json.load(f)
else:
    language_data = language_data_all

# 修正语言文件
for d in [language_data, language_data_all]:
    keys_to_remove = [
        key
        for key in d.keys()
        if key.startswith("item.minecraft.music_disc")
        or re.match(r"^item\.minecraft\.[^.]*_banner_pattern$", key)
    ]
    keys_to_remove.append("item.minecraft.smithing_template")

    for key in keys_to_remove:
        d.pop(key, None)

    updated_language_data = d.copy()

    for key, value in d.items():
        if "trim_smithing_template" in key:
            variant = key.split(".")[2].split("_", maxsplit=1)[0]
            variant_string = updated_language_data.get(
                f"trim_pattern.minecraft.{variant}", variant
            )
            updated_language_data[key] = f"{variant_string} Smithing Template"

    d.update(updated_language_data)

update_data = {
    "item.minecraft.netherite_upgrade_smithing_template": "Netherite Upgrade Smithing Template",
    "item.minecraft.music_disc_*": "Music Disc",
    "item.minecraft.*_banner_pattern": "Banner Pattern",
}

language_data_all.update(update_data)
if not NEW_STRINGS_ONLY:
    language_data.update(update_data)
