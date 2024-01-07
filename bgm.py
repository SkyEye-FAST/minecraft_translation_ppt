# -*- encoding: utf-8 -*-
"""添加背景音乐"""
from pathlib import Path

# 定义音频文件所在的文件夹路径
folder_path = Path(r"C:\Py-VSC\minecraft_translation_ppt\bgm")

# 获取文件夹中的所有音频文件
audio_files = sorted(list(folder_path.glob("*.mp3")))

# 构建FFmpeg命令
ffmpeg_command = ["ffmpeg"]


# 添加输入文件参数
for audio_file in audio_files:
    print(f"file '{audio_file}'")
