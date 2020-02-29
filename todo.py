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

from slugify import slugify

TITLE = HTML(
    """ <u>Todo Application</u>
 Press <b>'q'</b> to quit.

 To use TODO Application, type:
 'add' to add a todo item to TODO list.
 'mp [item index]' to move an item from TODO to In Progress.
 'mc [item index]' to move an item from In Progress to Completed.
 'del [todo item]' to remove an item from TODO list.
"""
)

title_height = 8

todo_list = []
inprogress_list = []
completed_list = []

input_field = TextArea(
    height=1,
    prompt=">>> ",
    style="class:input-field",
    multiline=False,
    wrap_lines=False,
    dont_extend_height=True,
)

column_info = [
    {"title": "TODO", "height": 4, "bg_color": "#70cb98", "fg_color": "#000000"},
    {"title": "In Progress", "height": 4, "bg_color": "#70cb98", "fg_color": "#000000"},
    {"title": "Completed", "height": 4, "bg_color": "#70cb98", "fg_color": "#000000"}
]


def create_headers(column_info):
    # Replace manual categories
    # column_info = {title: 'TODO', height: 4, bg_color: '#70cb98', fg_color: '#000000'}
    return [Window(
        FormattedTextControl(HTML(f"<u>{column['title']}</u>")),
        height=column['height'],
        ignore_content_width=True,
        style=f"bg:{column['bg_color']} {column['fg_color']} bold",
        align=WindowAlign.CENTER,
    ) for column in column_info]


def generate_fields(field_names):
    return [{field_name: TextArea(focusable=False, style="class:output-field")} for field_name in field_names]


def accept(buff):
    try:
        if input_field.text[:3] == "add":
            addTodo(input_field.text[4:])
        elif input_field.text[:2] == "mp":
            moveToInProgress(input_field.text[3])
        elif input_field.text[:2] == "mc":
            moveToCompleted(input_field.text[3])
        elif input_field.text[:3] == "del":
            deleteTodo(input_field.text[4:])
    except BaseException:
        return


input_field.accept_handler = accept


def addTodo(todo):
    todo_list.append(todo)
    refreshTodo(field_names[0])


def refreshTodo(todo_field):
    todo_text = ""
    for i in range(len(todo_list)):
        todo_text += "[" + str(i) + "] " + todo_list[i] + "\n"
    fields_list[0][todo_field].buffer.document = Document(text=todo_text)


def moveToInProgress(todo_index):
    item = todo_list[int(todo_index)]
    todo_list.pop(int(todo_index))
    refreshTodo(field_names[0])
    inprogress_list.append(item)
    refreshInProgress(field_names[1])


def refreshInProgress(inprogress_field):
    inprogress_text = ""
    for i in range(len(inprogress_list)):
        inprogress_text += "[" + str(i) + "] " + inprogress_list[i] + "\n"
    fields_list[1][inprogress_field].buffer.document = Document(text=inprogress_text)


def moveToCompleted(inprogress_index):
    item = inprogress_list[int(inprogress_index)]
    inprogress_list.pop(int(inprogress_index))
    refreshInProgress(field_names[1])
    completed_list.append(item)
    refreshCompleted(field_names[2])


def refreshCompleted(completed_field):
    completed_text = ""
    for i in range(len(completed_list)):
        completed_text += "[" + str(i) + "] " + completed_list[i] + "\n"
    fields_list[2][completed_field].buffer.document = Document(text=completed_text)


def deleteTodo(todo):
    # Check whether the todo item is in Todo, In Progress, or Completed
    # Remove the item from the list.
    if todo in todo_list:
        todo_list.remove(todo)
        refreshTodo()
    elif todo in inprogress_list:
        inprogress_list.remove(todo)
        refreshInProgress()
    elif todo in completed_list:
        completed_list.remove(todo)
        refreshCompleted()


def generate_columns(fields_list):
    return [Frame(
        HSplit(
            [field[key]],
            padding=field_style["padding"],
            padding_style=field_style["padding_style"],
            padding_char=field_style["padding_char"],
        )
    ) for field in fields_list for key in field.keys()]


def generate_body():
    return HSplit([title_frame, header_frame, columns_frame, line, input_field])


def generate_title():
    return Frame(Window(FormattedTextControl(TITLE), height=title_height), style=title_style)


def generate_header_frame():
    return VSplit(headers, height=1, padding=4, padding_style="bg:#000000",)


def generate_columns_frame():
    return  VSplit(
                columns,
                padding=1,
                padding_style="bg:#000000 #ffffff",
                padding_char=".",
            )


# 1. The layout
field_names = [f"{slugify(column['title'])}_field" for column in column_info]
fields_list = generate_fields(field_names)
field_style = {"padding": 1, "padding_style": "bg:#000000", "padding_char": "-"}
title_style = "bg:#000000 #ffffff"
headers = create_headers(column_info)
fields_list = generate_fields(field_names)
columns = generate_columns(fields_list)
title_frame = generate_title()
header_frame = generate_header_frame()
columns_frame = generate_columns_frame()
line = Window(height=1, char="-", style="class:line")
body = generate_body()

# 2. Key bindings
kb = KeyBindings()


@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()


# 3. The `Application`
application = Application(
    layout=Layout(body), key_bindings=kb, mouse_support=True, full_screen=True,
)


def run():
    application.run()


if __name__ == "__main__":
    run()
