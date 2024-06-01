# -*- encoding: utf-8 -*-
"""
自动复制模板幻灯片脚本，需要PowerPoint。
模拟手动复制粘贴操作，请不要在脚本运行过程中覆盖剪贴板。
"""

from typing import Callable

from win32com.client import Dispatch

from base import (
    PPT_DIR,
    IGNORE_CATEGORIES,
    is_valid_block,
    is_valid_entity,
    is_valid_item,
    language_data,
)


def copy_slide(
    category: str, key_prefix: str, validator: Callable[[str], bool]
) -> None:
    """
    复制幻灯片

    Args:
        category (str): 幻灯片类别
        key_prefix (str): 键前缀，用于筛选语言数据
        validator (Callable[[str], bool]): 验证函数，用于验证键是否有效
    """

    print(f"开始复制模板幻灯片，分类：{category}。")
    ppt = Dispatch("PowerPoint.Application")
    ppt.Visible = 1  # 后台运行
    ppt.DisplayAlerts = 0  # 不显示，不警告
    ppt_file = ppt.Presentations.Open(str(PPT_DIR / category / "template.pptx"))
    ppt_file.Slides(1).Copy()
    copy_num = sum(
        1 for key in language_data if key.startswith(key_prefix) and validator(key)
    )
    for _ in range(copy_num - 1):
        ppt_file.Slides.Paste()
    ppt_file.SaveAs(str(PPT_DIR / category / "copied.pptx"))
    ppt_file.Close()
    ppt.Quit()
    print("已完成。\n")


def main() -> None:
    """
    主函数，检查各类别是否被忽略，并调用对应的复制幻灯片函数
    """

    if not IGNORE_CATEGORIES["block"]:
        copy_slide("block", "", is_valid_block)
    if not IGNORE_CATEGORIES["entity"]:
        copy_slide("entity", "", is_valid_entity)
    if not IGNORE_CATEGORIES["item"]:
        copy_slide("item", "", is_valid_item)
    if not IGNORE_CATEGORIES["effect"]:
        copy_slide("effect", "effect.minecraft.", lambda x: True)
    if not IGNORE_CATEGORIES["enchantment"]:
        copy_slide("enchantment", "enchantment.minecraft.", lambda x: True)


if __name__ == "__main__":
    main()
