#!/usr/bin/env python
"""
In Progress: TODO App with new UI design.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Box, Frame, Label, TextArea

TITLE = HTML(
    """TODO App.
Press <b>'q'</b> to quit.
"""
)

input_field = TextArea(
    height=1,
    style="class:input-field",
    multiline=False,
    wrap_lines=False,
)

# 1. The layout
root_container = Box(
    HSplit([
        Label(text='Add TODO Items'),
        Frame(input_field),
    ])
)

layout = Layout(container=root_container)


# Key bindings.
kb = KeyBindings()


@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()


# 3. The `Application`
application = Application(
    layout=layout,
    key_bindings=kb,
    mouse_support=True,
    full_screen=True,
)


def run():
    application.run()


if __name__ == "__main__":
    run()
