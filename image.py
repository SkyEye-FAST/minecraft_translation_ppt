# -*- encoding: utf-8 -*-
"""从Minecraft Wiki获取等轴渲染图的脚本"""

import time
import json
import logging
import requests
from requests.exceptions import SSLError
from base import (
    LOG_DIR,
    IMAGE_DIR,
    IGNORE_BLOCK,
    IGNORE_ENTITY,
    IGNORE_ITEM,
    IGNORE_EFFECT,
    IGNORE_SAVED_IMAGE,
    is_valid_block,
    is_valid_entity,
    is_valid_item,
    language_data,
)

# 日志
LOG_DIR.mkdir(exist_ok=True)
log_file_name = f"image_download_{time.strftime('%Y%m%d%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / log_file_name, encoding="utf-8"),
    ],
)


def get_image_url(wiki_file_name: str):
    """获取Minecraft Wiki上图片原始文件的URL"""
    params = {
        "action": "query",
        "titles": f"File:{wiki_file_name}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    }

    response = requests.get("https://minecraft.wiki/api.php", params=params, timeout=60)
    data = response.json()

    # 获取图片信息
    pages = data["query"]["pages"]
    for page_info in pages.values():
        image_info = page_info.get("imageinfo", [])
        if image_info:
            return image_info[0]["url"]
    return None


sorted_items = [
    (key, value)
    for key, value in language_data.items()
    if (is_valid_block(key) and not IGNORE_BLOCK)
    or (is_valid_entity(key) and not IGNORE_ENTITY)
    or (is_valid_item(key) and not IGNORE_ITEM)
    or (key.startswith("effect.minecraft.") and not IGNORE_EFFECT)
]

# 创建图片文件夹（若不存在）
IMAGE_DIR.mkdir(exist_ok=True)

# 未获取到的图片
unknown = []

# 读取图片映射
with open(IMAGE_DIR / "image_mapping.json", "r", encoding="utf-8") as f:
    image_mapping = json.load(f)

for key, value in sorted_items:
    key_type = key.split(".")[0]
    (IMAGE_DIR / key_type).mkdir(exist_ok=True)

    file_name = f"{value}.png"

    file_path = IMAGE_DIR / key_type / file_name

    if file_path.is_file() and not IGNORE_SAVED_IMAGE:
        logging.info("%s已经存在。", file_name)
        continue

    url = (
        get_image_url(f"{value}_(item).png")
        if key_type == "item"
        else get_image_url(image_mapping.get(key, file_name))
    )
    if "Waxed" in value:
        url = get_image_url(f"{value[6:]}.png")
    if not url:
        url = get_image_url(image_mapping.get(key, file_name))

    # 获取图片
    if url:
        logging.info("正在获取图片%s。", file_name)
        logging.info("原始文件的URL：%s", url)
        try:
            with open(file_path, "wb") as f:
                f.write(requests.get(url, timeout=60).content)
            logging.info("图片已成功保存。")
        except SSLError as e:
            logging.error("遇到SSL错误：%s", e)
            logging.warning("服务器限制获取，将在15秒后尝试再次获取……")
            time.sleep(15)
            continue
    else:
        logging.warning("未找到%s。", file_name)
        unknown.append(file_name)

# 输出未找到的图片列表
if unknown:
    logging.warning("未找到的图片：")
    for i in unknown:
        logging.warning(i)
else:
    logging.info("所有图片已下载完成。")
