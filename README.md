# Minecraft中文标准译名列表视频生成器

[![Pylint](https://github.com/SkyEye-FAST/minecraft_translation_ppt/actions/workflows/pylint.yml/badge.svg)](https://github.com/SkyEye-FAST/minecraft_translation_ppt/actions/workflows/pylint.yml)

此项目用于生成Minecraft中文标准译名列表视频，载体为Microsoft PowerPoint。

视频最终效果参见[哔哩哔哩上的此视频](https://www.bilibili.com/video/BV1Si4y1z75m/)。

## 需求

由于使用了标准库`tomllib`，所以需要**Python >= 3.11**。

需要库[`requests`](https://github.com/psf/requests)、[`python-pptx`](https://github.com/scanny/python-pptx)、[`Pillow`](https://github.com/python-pillow/Pillow)和[`pypiwin32`](https://github.com/Googulator/pypiwin32)，请使用下面的命令安装：

``` shell
pip install requests python-pptx Pillow pypiwin32 -U
```

## 前期准备

### 语言文件

Java版语言文件请使用[SkyEye-FAST/minecraft_translation](https://github.com/SkyEye-FAST/minecraft_translation)获取。

请将获取到的`en_us.json`、`zh_cn.json`、`zh_hk.json`、`zh_tw.json`和`lzh.json`放置在语言文件文件夹下（默认为与脚本同级的`lang`文件夹，可以在配置文件中调整）。

[`supplements.json`](/lang/supplements.json)中存有目前（2024年1月7日）游戏内语言文件缺失，而Crowdin上已更新的内容。

## 脚本使用

### 获取图片

`image.py`用于从Minecraft Wiki获取等轴渲染图等图片。

获取到的图片默认保存在与脚本同级的`image`文件夹下的对应分类中，可以在配置文件中调整。此文件夹下的[`image_mapping.json`](/image/image_mapping.json)用于记录一些特殊情况，存有对应的图片映射。

获取图片的日志会默认保存在与脚本同级的`log`文件夹下，可以在配置文件中调整。

### 复制幻灯片

模板幻灯片文件已经在幻灯片文件夹（默认为与脚本同级的`ppt`文件夹，，可以在配置文件中调整）的对应分类下提供，名为`template.pptx`。由于模板幻灯片仅有一张，需要将其复制一定次数。

参考：[Slide.Copy 方法 (PowerPoint) | Microsoft Learn](https://learn.microsoft.com/zh-cn/office/vba/api/powerpoint.slide.copy)

#### Python

[`slide_copy.py`](/slide_copy.py)用于自动复制模板幻灯片，原理为模拟手动复制粘贴操作，请不要在此脚本运行过程中覆盖剪贴板。

此脚本运行需要**安装了PowerPoint的Windows设备**，且需要库[pywin32](https://github.com/mhammond/pywin32)（`pywin32`），请使用下面的命令安装：

```shell
pip install pywin32
```

#### VBA

[`slide_copy.bas`](/ppt/slide_copy.bas)可作为宏导入到需要复制的PowerPoint幻灯片文件中，并将其中循环变量的范围修改为需要的次数。

**此处不提供自动获取需要复制次数的功能，若有需要请自行在已有脚本基础上修改。**

### 查询翻译

[`slide.py`](/slide.py)用于自动填充幻灯片中的内容。

幻灯片按照源字符串的字母顺序排序。

## 设置动画

在自动填充幻灯片后，请根据需要拼接各个部分，并进行必要的修改与调整。

示例视频中使用的设置为：

1. 在“**切换**”选项卡上，选择“**平滑**”。
2. 选择“**切换**”>“**效果选项**”>“**文字**”。
3. 将持续时间设置为1s，自动换片时间设置为2s。

参考：[在 PowerPoint 中使用平滑切换 - Microsoft 支持](https://support.microsoft.com/zh-cn/office/%E5%9C%A8-powerpoint-%E4%B8%AD%E4%BD%BF%E7%94%A8%E5%B9%B3%E6%BB%91%E5%88%87%E6%8D%A2-8dd1c7b2-b935-44f5-a74c-741d8d9244ea)

## 导出视频

可以直接在PowerPoint中选择“**文件**”>“**导出**”>“**创建视频**”或“**录制**”>“**导出到视频**”，并选择所需要的设置来导出视频。

参考：[将演示文稿转换为视频 - Microsoft 支持](https://support.microsoft.com/zh-cn/office/%E5%B0%86%E6%BC%94%E7%A4%BA%E6%96%87%E7%A8%BF%E8%BD%AC%E6%8D%A2%E4%B8%BA%E8%A7%86%E9%A2%91-c140551f-cb37-4818-b5d4-3e30815c3e83)

[`video_output.bas`](/ppt/video_output.bas)可作为宏导入到需要导出的PowerPoint幻灯片文件中，来获取更高质量的视频。

脚本中视频参数为3840×2160，60FPS。

参考：[Presentation.CreateVideo 方法 (PowerPoint) | Microsoft Learn](https://learn.microsoft.com/zh-cn/office/vba/api/PowerPoint.Presentation.CreateVideo)

## 配置文件

配置文件名为`configuration.toml`，位置与脚本同级。

## 反馈

遇到的问题和功能建议等可以提出议题（Issue）。

欢迎创建拉取请求（Pull request）。
