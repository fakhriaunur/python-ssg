class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
            
        props_in_html = ""
        # fp
        # props_in_html += lambda prop: prop in self.props
        for prop in self.props:
            props_in_html += f' {prop}="{self.props[prop]}"'
        return props_in_html
    
    def __repr__(self):
        return (
            f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        )
    