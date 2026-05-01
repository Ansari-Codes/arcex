from Arcex.ax.Elements import Element

class Text(Element):
    def __init__(self, text, size=0, id = None):
        tag_map = {
            0: "p",
            1: "h1",
            2: "h2",
            3: "h3",
            4: "h4",
            5: "h5",
            6: "h6",
        }

        tag = tag_map.get(size, "p")
        super().__init__(tag, [{"__text__": text}], id)

    def set_text(self, text):
        for i, child in enumerate(self._children):
            if isinstance(child, dict):
                if isinstance(child, dict) and "__text__" in child:
                    child["__text__"] = str(text)
                    return self
        return self
