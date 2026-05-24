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
        # Shared Styles
        # =========================

        input_style = {
            "width": "100%",
            "padding": "14px",
            "border": "1px solid #334155",
            "border-radius": "12px",
            "background": "#1e293b",
            "color": "white",
            "font-size": "15px",
            "margin-bottom": "18px",
            "outline": "none",
            "transition": "0.2s ease"
        }

        label_style = {
            "font-size": "15px",
            "font-weight": "600",
            "margin-top": "15px",
            "margin-bottom": "8px",
            "color": "#cbd5e1",
            "display": "block"
        }

        section_style = {
            "background": "#111827",
            "padding": "24px",
            "border-radius": "18px",
            "margin-bottom": "25px",
            "border": "1px solid #334155",
            "box-shadow": "0 10px 30px rgba(0,0,0,0.25)"
        }

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
            styles={
                "background": "#0f172a",
                "min-height": "100vh",
                "padding": "40px",
                "font-family": "Inter, sans-serif",
                "color": "white"
            }
        ):

            Text(
                "✨ Interactive Dashboard",
                1,
                styles={
                    "font-size": "42px",
                    "font-weight": "700",
                    "margin-bottom": "10px"
                }
            )

            Text(
                "Modern UI using attrs, properties and styles",
                styles={
                    "color": "#94a3b8",
                    "margin-bottom": "30px"
                }
            )

            # =====================
            # Form Card
            # =====================

            with Element(
                "div",
                styles=section_style
            ):

                Text("📝 Description", styles=label_style)

                textarea = Textarea(
                    name="description",
                    value=self.state["text_value"],
                    rows=5,
                    attrs={
                        "placeholder": "Write something..."
                    },
                    styles=input_style,
                )

                textarea.on("input", on_text)

                Text("👤 Username", styles=label_style)

                inp = Input(
                    name="username",
                    value=self.state["text_value"],
                    attrs={
                        "placeholder": "Enter username..."
                    },
                    styles=input_style,
                )

                inp.on("input", on_text)

                Text("🎯 Select Option", styles=label_style)

                slc = Select(
                    name="choice",
                    options=["A", "B", "C", "D"],
                    value=self.state["selected_option"],
                    styles=input_style,
                )

                slc.on(on_select)

                Text("📅 Select Date", styles=label_style)

                date = Date(
                    name="date",
                    value=self.state["date_value"],
                    styles=input_style,
                )

                date.on(on_date)

                Text("🔢 Number", styles=label_style)

                num = Number(
                    name="quantity",
                    value=self.state["number_value"],
                    min=0,
                    max=100,
                    styles=input_style,
                )

                num.on("input", on_number)

                Text("📻 Radio", styles=label_style)

                radio = Radio(
                    name="radio",
                    options=[1, 2, 3, 4, 5],
                    value=self.state["radio_value"],
                    styles={
                        "margin-bottom": "20px"
                    },
                    id="radio-input"
                )

                radio.on(on_radio)

                check = Checkbox(
                    name="accept",
                    label="Accept Terms & Conditions",
                    checked=self.state["accepted"],
                    properties={
                        "required": True
                    },
                    styles={
                        "margin-top": "10px",
                        "margin-bottom": "20px"
                    },
                    id="checkbox-input"
                )

                check.on(on_check)

            # =====================
            # Counter Card
            # =====================

            with Element(
                "div",
                styles=section_style
            ):

                counter_text = Text(
                    f"🔥 Counter: {self.state['count']}",
                    2,
                    styles={
                        "font-size": "28px",
                        "font-weight": "700",
                        "color": "#facc15",
                        "margin-bottom": "20px"
                    },
                    id="text-inp"
                )

                btn = Button(
                    "Increment",
                    "inc-btn",
                    styles={
                        "background": "linear-gradient(135deg,#3b82f6,#2563eb)",
                        "color": "white",
                        "padding": "14px 22px",
                        "border": "none",
                        "border-radius": "14px",
                        "cursor": "pointer",
                        "font-size": "16px",
                        "font-weight": "600",
                        "transition": "0.2s ease"
                    },
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
                styles=section_style
            ):

                Text(
                    "📦 Live State",
                    2,
                    styles={
                        "margin-bottom": "15px",
                        "color": "#60a5fa"
                    },
                )

                display = Text(
                    "",
                    styles={
                        "white-space": "pre-wrap",
                        "font-family": "monospace",
                        "background": "#020617",
                        "padding": "18px",
                        "border-radius": "14px",
                        "line-height": "1.8",
                        "color": "#93c5fd"
                    },
                    id="display-text"
                )

        update_display()
