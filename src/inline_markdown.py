from textnode import TextNode, text_type_text


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        splitted_nodes = []
        sections = node.text.split(delimiter)
        
        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdown syntax, formatted section is not closed")
        
        for i, chunk in enumerate(sections):
            if i % 2 == 0:
                splitted_nodes.append(TextNode(chunk, text_type_text))
            else:
                splitted_nodes.append(TextNode(chunk, text_type))
        
        new_nodes.extend(splitted_nodes)

    return new_nodes