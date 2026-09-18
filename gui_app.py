from tkinter import *
from tkinter import filedialog, messagebox

WINDOW_BACKGROUND = "#A5D6A7"
BUTTON_BACKGROUND = "#66BB6A"
TEXT_BOX_BACKGROUND = "#E8F5E9"


class App(Tk):
    def __init__(self):
        super().__init__()

        self.time_elapsed = 0
        self.timer_id = None

        self.bind("<KeyPress>", self.reset_timer)

        self.title("Writing Block App")
        self.minsize(width=500, height=500)
        self.config(bg=WINDOW_BACKGROUND, padx=20, pady=20)

        self.start_label = Label(text="Start Writing.",
                                bg=WINDOW_BACKGROUND,
                                font=("Times", 24, "bold"))
        self.start_label.grid(row=0, column=0, columnspan=2)

        self.intro_label = Label(text="If you don't write anything for 5 seconds, everything will be deleted!",
                                bg=WINDOW_BACKGROUND,
                                font=("Times", 15, "italic"))
        self.intro_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.timer_label = Label(text="00:00",
                                bg=WINDOW_BACKGROUND,
                                font=("Times", 20, "bold"))
        self.timer_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.text_box = Text(bg=TEXT_BOX_BACKGROUND)
        self.text_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.text_box["state"] = "disabled"

        self.start_button = Button(text="Start",
                                bg=BUTTON_BACKGROUND,
                                font=("Times", 20, "bold"),
                                command=self.start_timer)
        self.start_button.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

        self.save_button = Button(text="Save",
                                bg=BUTTON_BACKGROUND,
                                font=("Times", 20, "bold"),
                                command=self.save_text)
        self.save_button.grid(row=4, column=1, columnspan=1, padx=10, pady=10)

    def start_timer(self):
        self.text_box["state"] = "normal"
        self.start_button["state"] = "disabled"
        self.update_timer()

    def update_timer(self):
        self.check_timer()
        seconds = self.time_elapsed % 60
        minutes = self.time_elapsed // 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.timer_id = self.after(1000, self.update_timer)
        self.time_elapsed += 1

    def reset_timer(self, event):
        self.time_elapsed = 0

    def check_timer(self):
        if self.time_elapsed == 5:
            self.text_box.delete("1.0", END)
            self.time_elapsed = 0

    def save_text(self):
        if self.timer_id is None:
            messagebox.showinfo(title="Oops!", message="Start writing first.")
            return
        self.after_cancel(self.timer_id)
        filepath = filedialog.asksaveasfilename(
            title="Save text",
            filetypes=[("Text files", "*.txt")],
            defaultextension=".txt")
        if not filepath:
            self.update_timer()
            return
        with open(filepath, mode="w") as file:
            file.write(self.text_box.get("1.0", END))
        self.update_timer()
