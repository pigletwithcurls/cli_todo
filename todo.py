#!/usr/bin/env python
"""
Vertical align demo with VSplit.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    HSplit,
    VerticalAlign,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame

TITLE = HTML(
    """<u>Todo Example</u> experiment.
 Press <b>'q'</b> to quit."""
)

LIPSUM = """
TODO EXAMPLE."""

todo_list = []
inprogress_list = []
completed_list = []


def addTodo(todo):
    if len(todo_list) >= 5:
        return
    todo_item = Window(
        BufferControl(Buffer(document=Document(todo))), height=2, style="bg:#000000"
    )
    todo_list.append(todo_item)


addTodo("Grocery shopping for family")
addTodo("Cook for lunch next week")

# 1. The layout
body = HSplit(
    [
        Frame(
            Window(FormattedTextControl(TITLE), height=2), style="bg:#000000 #ffffff"
        ),
        VSplit(
            [
                Window(
                    FormattedTextControl(HTML(" <u>TODO List</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#000000 #ffffff bold",
                    align=WindowAlign.CENTER,
                ),
                Window(
                    FormattedTextControl(HTML(" <u>In Progress</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#000000 #ffffff bold",
                    align=WindowAlign.CENTER,
                ),
                Window(
                    FormattedTextControl(HTML(" <u>TODO Completed</u>")),
                    height=4,
                    ignore_content_width=True,
                    style="bg:#000000 #ffffff bold",
                    align=WindowAlign.CENTER,
                ),
            ],
            height=1,
            padding=4,
            padding_style="bg:#000000",
        ),
        VSplit(
            [
                # TODO List
                Frame(
                    HSplit(
                        [
                            Window(
                                BufferControl(Buffer(document=Document(LIPSUM))),
                                height=6,
                                style="bg:#000000",
                            ),
                            Window(
                                BufferControl(Buffer(document=Document(LIPSUM))),
                                height=6,
                                style="bg:#000000",
                            ),
                            Window(
                                BufferControl(Buffer(document=Document(LIPSUM))),
                                height=6,
                                style="bg:#000000",
                            ),
                        ],
                        padding=1,
                        padding_style="bg:#000000",
                        padding_char="-",
                    )
                ),
                # In Progress
                Frame(
                    HSplit(
                        [
                            Window(
                                BufferControl(Buffer(document=Document(LIPSUM))),
                                height=6,
                                style="bg:#000000",
                            )
                        ],
                        padding=1,
                        padding_style="bg:#000000",
                        padding_char="-",
                    )
                ),
                # TODO Completed
                Frame(
                    HSplit(
                        [
                            Window(
                                BufferControl(Buffer(document=Document(""))),
                                height=6,
                                style="bg:#000000",
                            ),
                        ],
                        padding=1,
                        padding_style="bg:#000000",
                        padding_char="-",
                    )
                ),
            ],
            padding=1,
            padding_style="bg:#000000 #ffffff",
            padding_char=".",
        ),
    ]
)

# 2. Key bindings
kb = KeyBindings()


@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()


@kb.add("tab")
def _(event):
    event.app.layout.focus_next()


# 3. The `Application`
application = Application(layout=Layout(body), key_bindings=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()
