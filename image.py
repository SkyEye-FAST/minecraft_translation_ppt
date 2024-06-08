# -*- encoding: utf-8 -*-
"""从Minecraft Wiki获取等轴渲染图的脚本"""

import time
import json
import logging
from typing import Optional, List

import requests
from requests.exceptions import SSLError, ReadTimeout

from base import (
    LOG_DIR,
    IMAGE_DIR,
    IGNORE_CATEGORIES,
    IGNORE_SAVED_IMAGE,
    is_valid_key,
    language_data,
    Ldata,
    LdataTuple,
)


def get_image_url(wiki_file_name: str) -> Optional[str]:
    """
    获取Minecraft Wiki上图片原始文件的URL

    Args:
        wiki_file_name (str): Wiki文件名

    Returns:
        Optional[str]: 图片的URL，如果未找到则返回None
    """

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


if __name__ == "__main__":
    # 日志
    LOG_DIR.mkdir(exist_ok=True)
    log_file_name = f"image_download_{time.strftime('%Y%m%d%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_DIR / log_file_name, encoding="utf-8"),
        ],
    )

    sorted_items: LdataTuple = [
        (key, value)
        for key, value in language_data.items()
        if (is_valid_key(key, "block") and not IGNORE_CATEGORIES["block"])
        or (is_valid_key(key, "entity") and not IGNORE_CATEGORIES["entity"])
        or (is_valid_key(key, "item", "filled_map") and not IGNORE_CATEGORIES["item"])
        or (is_valid_key(key, "effect") and not IGNORE_CATEGORIES["effect"])
    ]

    # 创建图片文件夹（若不存在）
    IMAGE_DIR.mkdir(exist_ok=True)

    # 未获取到的图片
    unknown: List[str] = []

    # 读取图片映射
    with open(IMAGE_DIR / "image_mapping.json", "r", encoding="utf-8") as f:
        image_mapping: Ldata = json.load(f)

    for key, value in sorted_items:
        key_type = "item" if key.split(".")[0] == "filled_map" else key.split(".")[0]
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
        MAX_RETRIES = 3  # 最大重试次数
        if url:
            logging.info("正在获取图片%s。", file_name)
            logging.info("原始文件的URL：%s", url)

            RETRIES = 0
            while RETRIES < MAX_RETRIES:
                try:
                    with open(file_path, "wb") as f:
                        f.write(requests.get(url, timeout=60).content)
                    logging.info("图片已成功保存。")
                    break
                except SSLError as e:
                    logging.error("遇到SSL错误：%s", e)
                    if RETRIES < MAX_RETRIES - 1:
                        logging.warning("服务器限制获取，将在15秒后尝试再次获取……")
                        time.sleep(15)
                        RETRIES += 1
                    else:
                        logging.error("达到最大重试次数，终止操作。")
                        break
                except ReadTimeout as e:
                    logging.error("获取超时：%s", e)
                    if RETRIES < MAX_RETRIES - 1:
                        logging.warning("将在5秒后尝试再次获取……")
                        time.sleep(5)
                        RETRIES += 1
                    else:
                        logging.error("达到最大重试次数，终止操作。")
                        break
                except requests.exceptions.RequestException as e:
                    logging.error("请求异常：%s", e)
                    break
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
