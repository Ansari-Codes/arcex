from Arcex.ax.Elements import Element
import html as sanitizer

class Text(Element):
    def __init__(self, text, size=0, html=False, id=None):
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
        if html:safe_text = str(text)
        else:safe_text = sanitizer.escape(str(text))     
        super().__init__(tag, [{"__text__": safe_text}], id)

    def set_text(self, text):
        import html
        for child in self._children:
            if isinstance(child, dict) and "__text__" in child:
                child["__text__"] = html.escape(str(text))  # 🔥 ESCAPE HERE TOO
                return self
        return self
