class Element:
    _stack = []
    SELF_CLOSING = {"meta", "link", "input", "img", "br"}

    def __init__(
        self,
        _tag,
        children=None,
        id=None,
        attrs=None,
        properties=None,
        styles=None
    ):
        self._tag = _tag
        self._children = children or []

        self.attrs = attrs or {}
        self.properties = properties or {}
        self.styles = styles or {}

        if id:
            self.attrs["id"] = id

        self._id = id

        if Element._stack:
            Element._stack[-1]._children.append(self)

    def __enter__(self):
        Element._stack.append(self)
        return self

    def __exit__(self, exc_type, exc, tb):
        Element._stack.pop()

    def __html__(self):
        # normal attrs
        attr_parts = [
            f'{k}="{v}"'
            for k, v in self.attrs.items()
        ]

        # boolean attrs
        prop_parts = [
            k
            for k, v in self.properties.items()
            if v
        ]

        # inline styles
        if self.styles:
            style_str = "; ".join(
                f"{k}: {v}"
                for k, v in self.styles.items()
            )
            attr_parts.append(f'style="{style_str}"')

        attr_str = " ".join(attr_parts + prop_parts)

        inner = "".join(
            child.__html__() if hasattr(child, "__html__")
            else child["__text__"]
            if isinstance(child, dict) and "__text__" in child
            else str(child)
            for child in self._children
        )

        if self._tag in self.SELF_CLOSING:
            return f"<{self._tag} {attr_str}>"

        return f"<{self._tag} {attr_str}>{inner}</{self._tag}>"