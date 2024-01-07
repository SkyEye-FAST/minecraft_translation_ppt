# -*- encoding: utf-8 -*-
"""
自动复制模板幻灯片脚本，需要PowerPoint。
模拟手动复制粘贴操作，请不要在脚本运行过程中覆盖剪贴板。
"""

from win32com.client import Dispatch
from base import (
    PPT_DIR,
    IGNORE_BLOCK,
    IGNORE_ENTITY,
    IGNORE_ITEM,
    IGNORE_EFFECT,
    IGNORE_ENCHANTMENT,
    is_valid_block,
    is_valid_entity,
    is_valid_item,
    language_data,
)


def copy_slide(category: str, key_prefix: str, validator: bool):
    "复制幻灯片"
    print(f"开始复制模板幻灯片，分类：{category}。")
    ppt = Dispatch("PowerPoint.Application")
    ppt.Visible = 1  # 后台运行
    ppt.DisplayAlerts = 0  # 不显示，不警告
    ppt_file = ppt.Presentations.Open(PPT_DIR / category / "template.pptx")
    ppt_file.Slides(1).Copy()
    copy_num = sum(
        1 for key in language_data if key.startswith(key_prefix) and validator(key)
    )
    for _ in range(copy_num - 1):
        ppt_file.Slides.Paste()
    ppt_file.SaveAs(PPT_DIR / category / "copied.pptx")
    ppt_file.Close()
    ppt.Quit()
    print("已完成。\n")


if not IGNORE_BLOCK:
    copy_slide("block", "", is_valid_block)
if not IGNORE_ENTITY:
    copy_slide("entity", "", is_valid_entity)
if not IGNORE_ITEM:
    copy_slide("item", "", is_valid_item)
if not IGNORE_EFFECT:
    copy_slide("effect", "effect.minecraft.", lambda x: True)
if not IGNORE_ENCHANTMENT:
    copy_slide("enchantment", "enchantment.minecraft.", lambda x: True)
