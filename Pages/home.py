from Arcex.ax import Output, Page, Element
from Arcex.components import (LBreak, Text, Input, 
                            Select, Textarea, 
                            Checkbox, Number, 
                            Radio, Date, Button)

class HomePage(Page):
    route = '/'
    title = 'Home'
    favicon = "🙇‍♀️"

    def body(self):
        if "value" not in self.state:
            self.state.update({
                "text_value": "",
                "accepted": False,
                "selected_option": "A",
                "number_value": 0,
                "radio_value": 2,
                "date_value": ""
            })

        # ==================== Individual Handlers ====================

        def on_text_change(val):
            self.state["text_value"] = str(val)
            return update_display()

        def on_checkbox_change(checked):
            self.state["accepted"] = bool(checked)
            return update_display()

        def on_select_change(val):
            self.state["selected_option"] = str(val)
            return update_display()

        def on_number_change(val):
            self.state["number_value"] = val
            return update_display()

        def on_radio_change(val):
            self.state["radio_value"] = val
            return update_display()

        def on_date_change(val):
            self.state["date_value"] = str(val)
            return update_display()

        # Helper to update display
        def update_display():
            display_text = f"""
            {self.state}
            """      
            text.set_text(display_text)
            return Output().replace(text)
        
        # ==================== UI Structure ====================

        Text("Checks", 1)

        Text("Text Area")
        textarea = Textarea(name="description", value=self.state["text_value"], rows=5, id="desc")
        textarea.on("input", on_text_change)
        
        Text("Text Input")
        inp = Input(name="username", value=self.state["text_value"], id="input")
        inp.on("input", on_text_change)
        
        Text("Select")
        slc = Select(name="choice", options=["A", "B", "C", "D"], 
                    value=self.state["selected_option"], id="select")
        slc.on(on_select_change)

        Text("Date")
        date_input = Date(name="date", value=self.state["date_value"], id="date")
        date_input.on(on_date_change)
        
        chbox = Checkbox(name="accept", label="Do you accept the terms?", 
                        checked=self.state["accepted"], id="check")
        chbox.on(on_checkbox_change)
        
        Text("Number")
        num = Number(name="quantity", value=self.state["number_value"], 
                    min=0, max=100, id="number")
        num.on("input", on_number_change)
        
        Text("Radio Group")
        rad = Radio(name="radios", options=[1, 2, 3, 4, 5], 
                    value=self.state["radio_value"], id="radios")
        rad.on(on_radio_change)
        
        self.state['count'] = 0
        t = Text(f"Count: {self.state['count']}", 1, id='counter-label')
        
        def inc(e=None):
            self.state['count'] += 1
            t.set_text("Count: " + self.state['count'].__str__())
            print(self.state['count'])
            return Output().replace(t)
        
        Button("Increment", "inc-btn").onclick(inc)

        Element("hr")
        text = Text("", 2, id="text")

        # Initial render
        update_display()
