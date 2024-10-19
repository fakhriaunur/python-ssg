from typing import List

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    return list(filter(None, map(str.strip, blocks)))
    # filtered_blocks = []
    # for block in blocks:
    #     if not block:
    #         continue
    #     stripped_block = block.strip()
    #     filtered_blocks.append(stripped_block)
    # return filtered_blocks
