from Arcex.ax import Output, Page
from Arcex.components import (
    Element, Text, Input,
    Select, Textarea,
    Checkbox, Number,
    Radio, Date, Button
)

class HomePage(Page):

    route = '/'
    title = 'Interactive UI'
    favicon = '✨'

    def body(self):

        # =========================
        # Initialize State
        # =========================

        if "initialized" not in self.state:

            self.state.update({
                "initialized": True,
                "text_value": "",
                "accepted": False,
                "selected_option": "A",
                "number_value": 0,
                "radio_value": 1,
                "date_value": "",
                "count": 0
            })

        # =========================
        # Update Display
        # =========================

        def update_display():

            content = f"""
Text Value: {self.state['text_value']}

Accepted: {self.state['accepted']}

Selected: {self.state['selected_option']}

Number: {self.state['number_value']}

Radio: {self.state['radio_value']}

Date: {self.state['date_value']}

Count: {self.state['count']}
            """

            display.set_text(content)

            counter_text.set_text(
                f"🔥 Counter: {self.state['count']}"
            )

            return Output() \
                .replace(display) \
                .replace(counter_text)

        # =========================
        # Handlers
        # =========================

        def on_text(val):
            self.state["text_value"] = str(val)
            return update_display()

        def on_check(val):
            self.state["accepted"] = bool(val)
            return update_display()

        def on_select(val):
            self.state["selected_option"] = str(val)
            return update_display()

        def on_number(val):
            self.state["number_value"] = val
            return update_display()

        def on_radio(val):
            self.state["radio_value"] = val
            return update_display()

        def on_date(val):
            self.state["date_value"] = str(val)
            return update_display()

        def increment(e=None):

            self.state["count"] += 1

            return update_display()

        # =========================
        # Page Container
        # =========================

        with Element(
            "div",
        ):

            Text(
                "✨ Interactive Dashboard",
                1
            )

            Text(
                "Modern UI using attrs, properties and styles",
            )

            # =====================
            # Form Card
            # =====================

            with Element(
                "div",
            ):

                Text("📝 Description")

                textarea = Textarea(
                    name="description",
                    value=self.state["text_value"],
                    rows=5,
                    attrs={
                        "placeholder": "Write something..."
                    },
                )

                textarea.on("input", on_text)

                Text("👤 Username")

                inp = Input(
                    name="username",
                    value=self.state["text_value"],
                    attrs={
                        "placeholder": "Enter username..."
                    },
                )

                inp.on("input", on_text)

                Text("🎯 Select Option")

                slc = Select(
                    name="choice",
                    options=["A", "B", "C", "D"],
                    value=self.state["selected_option"],
                )

                slc.on(on_select)

                Text("📅 Select Date")

                date = Date(
                    name="date",
                    value=self.state["date_value"],
                )

                date.on(on_date)

                Text("🔢 Number")

                num = Number(
                    name="quantity",
                    value=self.state["number_value"],
                    min=0,
                    max=100,
                )

                num.on("input", on_number)

                Text("📻 Radio")

                radio = Radio(
                    name="radio",
                    options=[1, 2, 3, 4, 5],
                    value=self.state["radio_value"],
                )

                radio.on(on_radio)

                check = Checkbox(
                    name="accept",
                    label="Accept Terms & Conditions",
                    checked=self.state["accepted"],
                    properties={
                        "required": True
                    },
                )

                check.on(on_check)

            # =====================
            # Counter Card
            # =====================

            with Element(
                "div",
            ):

                counter_text = Text(
                    f"🔥 Counter: {self.state['count']}",
                    2,
                )

                btn = Button(
                    "Increment",
                    attrs={
                        "title": "Increase counter"
                    }
                )

                btn.onclick(increment)

            # =====================
            # State Viewer
            # =====================

            with Element(
                "div",
            ):

                Text(
                    "📦 Live State",
                    2,
                )

                display = Text(
                    "",
                )

        update_display()
