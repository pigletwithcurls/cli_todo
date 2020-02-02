#!/usr/bin/env python
"""
Vertical align demo with VSplit.
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
from prompt_toolkit.widgets import Frame, TextArea

TITLE = HTML(
    """ <u>Todo Application</u>
 Press <b>'q'</b> to quit.

 To use TODO Application, type:
 'add' to add a todo item to TODO list.
 'mp [item index]' to move an item from TODO to In Progress.
 'mc [item index]' to move an item from In Progress to Completed.
 """
)

todo_list = []
inprogress_list = []
completed_list = []

input_field = TextArea(
    height=1,
    prompt=">>> ",
    style="class:input-field",
    multiline=False,
    wrap_lines=False,
)

todo_field = TextArea(style="class:output-field")
inprogress_field = TextArea(style="class:output-field")
completed_field = TextArea(style="class:output-field")

categories = [
    Window(
        FormattedTextControl(HTML("<u>TODO</u>")),
        height=4,
        ignore_content_width=True,
        style="bg:#70cb98 #000000 bold",
        align=WindowAlign.CENTER,
    ),
    Window(
        FormattedTextControl(HTML("<u>In Progress</u>")),
        height=4,
        ignore_content_width=True,
        style="bg:#70cb98 #000000 bold",
        align=WindowAlign.CENTER,
    ),
    Window(
        FormattedTextControl(HTML("<u>Completed</u>")),
        height=4,
        ignore_content_width=True,
        style="bg:#70cb98 #000000 bold",
        align=WindowAlign.CENTER,
    ),
]

field_style = {"padding": 1, "padding_style": "bg:#000000", "padding_char": "-"}
title_style = "bg:#000000 #ffffff"


def accept(buff):
    try:
        if input_field.text[:3] == "add":
            addTodo(input_field.text[4:])
        elif input_field.text[:2] == "mp":
            moveToInProgress(input_field.text[3])
        elif input_field.text[:2] == "mc":
            moveToCompleted(input_field.text[3])
    except BaseException as e:
        print("\nError", e)


input_field.accept_handler = accept


def addTodo(todo):
    todo_list.append(todo)
    refreshTodo()


def refreshTodo():
    todo_text = ""
    for i in range(len(todo_list)):
        todo_text += "[" + str(i) + "] " + todo_list[i] + "\n"
    todo_field.buffer.document = Document(text=todo_text)


def moveToInProgress(todo_index):
    item = todo_list[int(todo_index)]
    todo_list.pop(int(todo_index))
    refreshTodo()
    inprogress_list.append(item)
    refreshInProgress()


def refreshInProgress():
    inprogress_text = ""
    for i in range(len(inprogress_list)):
        inprogress_text += "[" + str(i) + "] " + inprogress_list[i] + "\n"
    inprogress_field.buffer.document = Document(text=inprogress_text)


def moveToCompleted(inprogress_index):
    item = inprogress_list[int(inprogress_index)]
    inprogress_list.pop(int(inprogress_index))
    refreshInProgress()
    completed_list.append(item)
    refreshCompleted()


def refreshCompleted():
    completed_text = ""
    for i in range(len(completed_list)):
        completed_text += "[" + str(i) + "] " + completed_list[i] + "\n"
    completed_field.buffer.document = Document(text=completed_text)


# 1. The layout
body = HSplit(
    [
        Frame(Window(FormattedTextControl(TITLE), height=7), style=title_style),
        VSplit(categories, height=1, padding=4, padding_style="bg:#000000",),
        VSplit(
            [
                # TODO List
                Frame(
                    HSplit(
                        [todo_field],
                        padding=field_style["padding"],
                        padding_style=field_style["padding_style"],
                        padding_char=field_style["padding_char"],
                    )
                ),
                # In Progress
                Frame(
                    HSplit(
                        [inprogress_field],
                        padding=field_style["padding"],
                        padding_style=field_style["padding_style"],
                        padding_char=field_style["padding_char"],
                    )
                ),
                # TODO Completed
                Frame(
                    HSplit(
                        [completed_field],
                        padding=field_style["padding"],
                        padding_style=field_style["padding_style"],
                        padding_char=field_style["padding_char"],
                    )
                ),
            ],
            padding=1,
            padding_style="bg:#000000 #ffffff",
            padding_char=".",
        ),
        Window(height=1, char="-", style="class:line"),
        input_field,
    ]
)

# 2. Key bindings
kb = KeyBindings()


@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()


# 3. The `Application`
application = Application(
    layout=Layout(body, focused_element=input_field),
    key_bindings=kb,
    mouse_support=True,
    full_screen=True,
)


def run():
    application.run()


if __name__ == "__main__":
    run()
