
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("966x630")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 630,
    width = 966,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    129.5,
    147.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=90.0,
    y=128.0,
    width=79.0,
    height=37.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    688.5,
    339.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_2.place(
    x=444.0,
    y=128.0,
    width=489.0,
    height=420.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    129.5,
    253.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_3.place(
    x=90.0,
    y=234.0,
    width=79.0,
    height=37.0
)

canvas.create_text(
    80.0,
    97.0,
    anchor="nw",
    text="Port Forward:",
    fill="#000000",
    font=("Roboto", 12 * -1)
)

canvas.create_text(
    439.0,
    97.0,
    anchor="nw",
    text="Output",
    fill="#000000",
    font=("Roboto", 12 * -1)
)

canvas.create_text(
    80.0,
    200.0,
    anchor="nw",
    text="Log file:",
    fill="#000000",
    font=("Roboto", 12 * -1)
)

canvas.create_text(
    80.0,
    172.0,
    anchor="nw",
    text="(Defualt is 2222)",
    fill="#828282",
    font=("Roboto", 12 * -1)
)

canvas.create_text(
    80.0,
    278.0,
    anchor="nw",
    text="(Defualt is stinger.log)",
    fill="#828282",
    font=("Roboto", 12 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=80.0,
    y=502.0,
    width=99.0,
    height=40.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=200.0,
    y=502.0,
    width=99.0,
    height=40.0
)

canvas.create_text(
    80.0,
    18.0,
    anchor="nw",
    text="Stinger",
    fill="#F2C94C",
    font=("Roboto", 64 * -1)
)
window.resizable(False, False)
window.mainloop()
