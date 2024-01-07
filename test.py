import re


def is_valid_block(block_key: str):
    """判断是否为有效方块键名"""
    if block_key.startswith("block.") and not re.match(
        r"block\.minecraft\.(.*)\.", block_key
    ):
        return True
    else:
        return False


a = input()
print(is_valid_block(a))
