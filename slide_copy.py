# -*- encoding: utf-8 -*-
"""
自动复制模板幻灯片脚本，需要PowerPoint。
模拟手动复制粘贴操作，请不要在脚本运行过程中覆盖剪贴板。
"""

from win32com.client import Dispatch

from base import (
    PPT_DIR,
    IGNORE_CATEGORIES,
    is_valid_key,
    language_data,
)


def copy_slide(*category: str) -> None:
    """
    复制幻灯片

    Args:
        category (str): 类别
        validator (Optional[Callable[[str], bool]]): 验证函数，用于验证键是否有效；默认为None
    """

    print(f"开始复制模板幻灯片，分类：{category[0]}。")
    dir_c = PPT_DIR / category[0]
    ppt = Dispatch("PowerPoint.Application")
    ppt.DisplayAlerts = 0  # 不显示，不警告
    copy_num = sum(1 for key in language_data if is_valid_key(key, *category))
    if copy_num == 0:
        print(f"不存在分类为{category[0]}的字符串。\n")
    else:
        template_path = str(dir_c / "template.pptx")
        ppt_file = ppt.Presentations.Open(template_path, True, False, False)
        ppt_file.Slides(1).Copy()
        for _ in range(copy_num - 1):
            ppt_file.Slides.Paste()
        ppt_file.SaveAs(str(dir_c / "copied.pptx"))
        ppt_file.Close()
        ppt.Quit()
        print("已完成。\n")


def main() -> None:
    """
    主函数，检查各类别是否被忽略，并调用对应的复制幻灯片函数
    """
    if not IGNORE_CATEGORIES["advancements"]:
        copy_slide("advancements")
    if not IGNORE_CATEGORIES["biome"]:
        copy_slide("biome")
    if not IGNORE_CATEGORIES["block"]:
        copy_slide("block")
    if not IGNORE_CATEGORIES["entity"]:
        copy_slide("entity")
    if not IGNORE_CATEGORIES["item"]:
        copy_slide("item", "filled_map")
    if not IGNORE_CATEGORIES["effect"]:
        copy_slide("effect")
    if not IGNORE_CATEGORIES["enchantment"]:
        copy_slide("enchantment")


if __name__ == "__main__":
    main()
