from arcex.ax import Output, Page
from arcex.components import Text, Button, Input, Select


class HomePage(Page):
    route = '/'
    title = 'Home'
    favicon = "🙇‍♀️"

    def body(self):

        if "count" not in self.state:
            self.state["count"] = 0

        if "name" not in self.state:
            self.state["name"] = ""

        # text display
        t = Text(
            f"Hello {self.state['name']} | Count: {self.state['count']}",
            2,
            id="text"
        )

        # button click
        def change_text(_):
            self.state['count'] += 1

            t.set_text(
                f"Hello {self.state['name']} | Count: {self.state['count']}"
            )

            return Output().replace(t)

        # input change
        def change_text_input(inp_val):
            self.state["name"] = inp_val

            t.set_text(
                f"Hello {inp_val} | Count: {self.state['count']}"
            )

            return Output().replace(t)

        # input field
        inp = Input(
            name="username",
            value=self.state["name"],
            id="name_input",
        )
        inp.onchange("enter", change_text_input)

        # button
        Button("Click", onclick=change_text, id="btn")

        # dynamic event switching
        def change_input_work(mode):
            inp.onchange(mode, change_text_input)

            return Output().replace(inp)

        # select
        slc = Select(
            name="way",
            options=[
                ("Live Input", "input"),
                ("Enter", "enter"),
                ("Key Down", "keydown"),
                ("Key Up", "keyup")
            ],
            value="enter",
            id="way",
        )
        slc.onchange(change_input_work)