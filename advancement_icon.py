# -*- encoding: utf-8 -*-
"""为进度添加图标"""

import json
from pptx import Presentation as prstt
from pptx.util import Cm
from base import P, PPT_DIR, IMAGE_DIR, sort_data, load_language_files

with open(P / "advancements_data.json", "r", encoding="utf-8") as f:
    data_adv = json.load(f)

file_list = ["en_us.json", "zh_cn.json", "zh_hk.json", "zh_tw.json", "lzh.json"]
sorted_data = sort_data(load_language_files(file_list), "advancements")["en_us"]

prs_path = PPT_DIR / "advancements" / "output.pptx"
prs = prstt(prs_path)

for n, slide in enumerate(prs.slides):
    key = sorted_data[n][0]
    img_path = IMAGE_DIR / "advancements" / f"{data_adv[key]["frame"]}.png"
    slide.shapes.add_picture(
        image_file=str(img_path),
        left=Cm(25.96),
        top=Cm(7.4),
        width=Cm(5),
        height=Cm(5),
    )

prs.save(PPT_DIR / "advancements" / "output.pptx")
