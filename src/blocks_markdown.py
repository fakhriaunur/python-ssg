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

def block_to_block_type(markdown: str) -> str:
    lines = markdown.split("\n")
    first_line = lines[0]
    
    pound_count = first_line.count("#", 0, 6)
    if 1 <= pound_count <= 6 and first_line[pound_count] == " ":
        return "heading"
    
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return "code"
    
    if all(line.startswith(">") for line in lines):
        return "quote"
    
    if all(line.startswith("*") or line.startswith("-") for line in lines):
        return "unordered_list"
    
    if all(line.strip() for line in lines):
        current_numbering = 1
        for line in lines:
            parts = line.split(".", 1)
            if len(parts) != 2:
                return "paragraph"
            
            number_part, rest = parts
            
            if not number_part.strip().isdigit():
                return "paragrah"
            
            if int(number_part) != current_numbering:
                return "paragraph"
            
            if not rest.startswith(" "):
                return "paragraph"
            
            current_numbering += 1
        
        return "ordered_list"
    
    return "paragraph"