from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Must have a tag")
        
        if self.children is None:
            raise ValueError("Must have at least a child")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html
        
        return (
            f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        )
    
    def __repr__(self):
        return (
            f"ParentNode({self.tag}, {self.children}, {self.props})"
        )