from Arcex.ax import Output, Page
from Arcex.components import Text, Date, Input, Select, Textarea, Checkbox, Number, Radio

class HomePage(Page):
    route = '/'
    title = 'Home'
    favicon = "🙇‍♀️"

    def body(self):
        if 'value' not in self.state:
            self.state["value"] = ""
        def on_text_change(val):
            self.state["value"] = val
            if chbox._checked:
                text.set_text(self.state['value'])
            else:
                text.set_text("Enable it first!")
            return Output().replace(text)
        
        textarea = Textarea(name="description", value=self.state['value'], rows=6, id="desc")
        textarea.on("input", on_text_change)
        
        inp = Input(name="input", value=self.state['value'], id="input")
        inp.on("input", on_text_change)
        
        slc = Select("select", ["A", "B", "C", "D"], "A", id="select")
        slc.on(on_text_change)
        
        date = Date("date", id="date")
        date.on(on_text_change)
        
        chbox = Checkbox("checkbox", "Do you accept?", id="check")
        chbox.on(on_text_change)
        
        num = Number("number", id="number")
        num.on('input', on_text_change)
        
        rad = Radio("radios", [1, 2, 3, 4], 2, "radios")
        rad.on(on_text_change)

        text = Text(self.state['value'], 2, id="text")
        
