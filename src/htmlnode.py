import html

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        if self.props:  # Handle attributes like props
            props_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            open_tag = f"<{self.tag} {props_str}>"
        else:
            open_tag = f"<{self.tag}>"
        children_str = ''.join(child.to_html() for child in self.children)
        close_tag = f"</{self.tag}>"
        return f"{open_tag}{children_str}{close_tag}"

    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{html.escape(str(value))}"' for key, value in self.props.items())
    
    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})"
        )
    
    def add_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag specified for the HTML node.")
        if self.children is None:
            raise ValueError("Children attribute cannot be None.")
        if not all(isinstance(child, HTMLNode) for child in self.children):
            raise TypeError("All children must be instances of HTMLNode.")
        children = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children}</{self.tag}>'
    
    def add_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)
