# -*- encoding: utf-8 -*-
"""自动化生成Minecraft标准译名列表所用脚本，列表载体为PowerPoint幻灯片。"""

import json
import re
from PIL import Image
from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from base import (
    LANG_DIR,
    IMAGE_DIR,
    PPT_DIR,
    SLIDE_CONFIG,
    IGNORE_BLOCK,
    IGNORE_ENTITY,
    IGNORE_ITEM,
    IGNORE_EFFECT,
    IGNORE_ENCHANTMENT,
    is_valid_block,
    is_valid_entity,
    is_valid_item,
)

# 读取语言文件
print("开始读取语言文件。")
file_list = [
    "en_us.json",
    "zh_cn.json",
    "zh_hk.json",
    "zh_tw.json",
    "lzh.json",
]
data = {}
for file in file_list:
    with open(LANG_DIR / file, "r", encoding="utf-8") as f:
        data[file.split(".", maxsplit=1)[0]] = json.load(f)

# 修正语言文件
updated_data = data

for lang in ["en_us", "zh_cn", "zh_hk", "zh_tw", "lzh"]:
    netherite_upgrade_str = data[lang]["upgrade.minecraft.netherite_upgrade"]
    smithing_template_str = data[lang]["item.minecraft.smithing_template"]
    music_disc_str = data[lang]["item.minecraft.music_disc_5"]
    banner_pattern_str = data[lang]["item.minecraft.mojang_banner_pattern"]
    updated_data[lang]["item.minecraft.netherite_upgrade_smithing_template"] = (
        netherite_upgrade_str + " " + smithing_template_str
        if lang == "en_us"
        else netherite_upgrade_str + smithing_template_str
    )
    trim_keys = [key for key in data[lang].keys() if "trim_smithing_template" in key]
    keys_to_add = {
        key: data[lang][
            f"trim_pattern.minecraft.{key.split('.')[2].split('_', maxsplit=1)[0]}"
        ]
        + " "
        + smithing_template_str
        if lang == "en_us"
        else data[lang][
            f"trim_pattern.minecraft.{key.split('.')[2].split('_', maxsplit=1)[0]}"
        ]
        + smithing_template_str
        for key in trim_keys
    }
    updated_data[lang].update(keys_to_add)

    keys_to_delete = [
        key
        for key in data[lang].keys()
        if key.startswith("item.minecraft.music_disc")
        or re.match(r"item\.minecraft\.(.*)_banner_pattern", key)
    ]
    for key in keys_to_delete:
        del updated_data[lang][key]
    del updated_data[lang]["item.minecraft.smithing_template"]

    updated_data[lang]["item.minecraft.music_disc_*"] = music_disc_str
    updated_data[lang]["item.minecraft.*_banner_pattern"] = banner_pattern_str

data = updated_data

# 读取补充字符串
with open(LANG_DIR / "supplements.json", "r", encoding="utf-8") as f:
    supplements = json.load(f)
for lang in ["zh_cn", "zh_hk", "zh_tw", "lzh"]:
    data[lang].update(supplements[lang])
print(f"已补充{len(supplements['zh_cn'])}条字符串。")


def edit_text(slide_data: dict, category: str, prs):
    """编辑幻灯片文本"""
    print(f"开始编辑幻灯片文本，分类：{category}。")

    for n, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            # 编辑文本框
            if shape.has_text_frame:
                tf = shape.text_frame
                # 源字符串
                if tf.text == "Source String":
                    tf.text = slide_data["en_us"][n][1]
                    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
                    tf.paragraphs[0].font.name = SLIDE_CONFIG["font"]["source"]
                    tf.paragraphs[0].font.size = Pt(SLIDE_CONFIG["size"]["source"])
                # 本地化键名
                if tf.text == "Translation Key":
                    tf.text = slide_data["en_us"][n][0]
                    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
                    tf.paragraphs[0].font.name = SLIDE_CONFIG["font"]["translation_key"]
                    tf.paragraphs[0].font.size = Pt(
                        SLIDE_CONFIG["size"]["translation_key"]
                    )
            # 编辑表格
            if shape.has_table:
                table = shape.table

                for i, lang_name in enumerate(
                    ["zh_cn", "zh_hk", "zh_tw", "lzh"], start=1
                ):
                    table.cell(i, 1).text = slide_data[lang_name][n][1]
                    cell = table.cell(i, 1).text_frame.paragraphs[0]
                    cell.font.name = SLIDE_CONFIG["font"][lang_name]
                    cell.font.bold = SLIDE_CONFIG["bold"][lang_name]
                    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                    cell.alignment = PP_ALIGN.CENTER
                    cell.font.size = Pt(SLIDE_CONFIG["size"][lang_name])


def add_image(slide_data: dict, category: str, prs):
    """在幻灯片中添加图片"""
    print(f"开始添加图片，分类：{category}。")

    for n, slide in enumerate(prs.slides):
        # 添加图片
        img_path = str(IMAGE_DIR / category / f"{slide_data['en_us'][n][1]}.png")
        img_size = Image.open(img_path).size

        img_height = img_size[1] / 720 * 19.05
        img_width = img_size[0] / 720 * 19.05
        if img_height > 12:
            img_width = img_width * 11.5 / img_height
            img_height = 11.5
        if img_width > 8:
            img_height = img_height * 8 / img_width
            img_width = 8

        slide.shapes.add_picture(
            image_file=img_path,
            left=Cm(28.57 - img_width / 2),
            top=Cm((19.05 - img_height) / 2 + 0.38),
            width=Cm(img_width),
            height=Cm(img_height),
        )


def edit_slide(slide_data: dict, category: str):
    """编辑幻灯片"""
    prs = Presentation(PPT_DIR / category / "copied.pptx")
    edit_text(slide_data, category, prs)
    if category != "enchantment":
        add_image(slide_data, category, prs)
    prs.save(PPT_DIR / category / "output.pptx")


def sort_data(lang_data: dict, key_prefix: str, validator: bool):
    """排序语言数据"""
    sorted_data = {
        "en_us": sorted(
            (
                (key, value)
                for key, value in lang_data["en_us"].items()
                if key.startswith(key_prefix) and validator(key)
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
                if key.startswith(key_prefix) and validator(key)
            ),
            key=lambda x: sorted_keys.index(x[0]),
        )
    return sorted_data


# 生成内容
print("开始生成幻灯片内容。")

if not IGNORE_BLOCK:
    sorted_data_block = sort_data(data, "", is_valid_block)
    edit_slide(sorted_data_block, "block")
if not IGNORE_ENTITY:
    sorted_data_entity = sort_data(data, "", is_valid_entity)
    edit_slide(sorted_data_entity, "entity")
if not IGNORE_ITEM:
    sorted_data_item = sort_data(data, "", is_valid_item)
    edit_slide(sorted_data_item, "item")
if not IGNORE_EFFECT:
    sorted_data_effect = sort_data(data, "effect.minecraft.", lambda x: True)
    edit_slide(sorted_data_effect, "effect")
if not IGNORE_ENCHANTMENT:
    sorted_data_enchantment = sort_data(data, "enchantment.minecraft.", lambda x: True)
    edit_slide(sorted_data_enchantment, "enchantment")

print("已完成。")
