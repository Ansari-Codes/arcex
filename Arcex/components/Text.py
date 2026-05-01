from Arcex.ax.Elements import Element
from Arcex.ax.Exceptions import AXError
import markdown

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

class Code(Element):
    def __init__(self, code: str = "", language: str = "", id: str|None = None):
        self._code = code
        self._language = language
        if language:
            code_element = Element("code", [{"__text__": str(code)}], 
                                attrs={"class": f"language-{language}"})
            super().__init__("pre", [code_element], id=id)
        else:
            super().__init__("pre", [{"__text__": str(code)}], id=id)

    def set_code(self, code: str):
        self._code = code

        if self._children and isinstance(self._children[0], Element) and self._children[0]._tag == "code":
            inner = self._children[0]
            for i, child in enumerate(inner._children):
                if isinstance(child, dict) and "__text__" in child:
                    child["__text__"] = str(code)
                    return self
        else:
            for i, child in enumerate(self._children):
                if isinstance(child, dict) and "__text__" in child:
                    child["__text__"] = str(code)
                    return self

        return self

    def set_language(self, language: str):
        self._language = language
        return self
    
class Markdown(Element):
    def __init__(self, markdown_text: str = "", id: str|None = None):
        self._markdown_text = markdown_text
        self._html_content = self._convert_to_html(markdown_text)
        super().__init__("div", [{"__text__": self._html_content}], id=id, 
                        attrs={"class": "markdown-body"})

    def _convert_to_html(self, md_text: str) -> str:
        try:
            extensions = ["fenced_code", "tables", "nl2br"]
            return markdown.markdown(md_text, extensions=extensions)
        except Exception:
            raise AXError("markdown library is not installed (or corrupted). Reinstall it using: \n\t`pip install markdown`")

    def set_markdown(self, markdown_text: str):
        self._markdown_text = markdown_text
        self._html_content = self._convert_to_html(markdown_text)

        for child in self._children:
            if isinstance(child, dict) and "__text__" in child:
                child["__text__"] = self._html_content
                break
        return self

    def set_text(self, text: str):
        return self.set_markdown(text)
