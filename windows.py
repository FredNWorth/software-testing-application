from tkinter import Label, Toplevel
from app_brain import delete_element
from easygui import ccbox

BACKGROUND_COLOUR = "#91c9c0"
GEOMETRY = "400x700"
HEADER_FONT = ("Arial", 18, "bold")


class Window:
    """Opens a new window to explore the selected project.
    uses tkinter Toplevel to reference the root (i.e. HomeUI)"""

    def delete_from_ui(self, element_id, delete_type):
        check_sure = ccbox(title=f"Delete {delete_type}",
                           msg=f"Are you sure you wand to delete this {delete_type}?")
        if check_sure:
            ui_button = self.this_window.nametowidget(f'{delete_type}: {element_id}')
            ui_delete_button = self.this_window.nametowidget(f'{element_id}')
            ui_button.destroy()
            ui_delete_button.destroy()
            delete_element(delete_type, element_id)

    def __init__(self, heading, root):
        self.heading = heading
        self.this_window = Toplevel(root, padx=20, name=f'proj_{heading}')
        self.this_window.geometry(GEOMETRY)
        self.this_window.title(heading)
        self.this_window.config(background=BACKGROUND_COLOUR)
        self.page_title = Label(self.this_window,
                                text=heading,
                                font=HEADER_FONT,
                                background=BACKGROUND_COLOUR,
                                pady=20)
        self.page_title.grid(row=0, column=0, columnspan=3)
