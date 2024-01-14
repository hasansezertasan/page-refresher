from tkinter import Button, Entry, Label, Tk, W


class Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Page Refresher")
        self.wm_geometry("600x300")
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        self.wm_resizable(False, False)
        self.configure(bg="white")

        self.interface()

    def interface(self):
        self.link_label = Label(
            text="Target URL:",
            bg="white",
            fg="black",
            font="none 12 bold",
            width=25,
        )
        self.link_label.grid(row=1, column=0, stick=W)

        self.delay_label = Label(
            text="Refresh Delay:",
            bg="white",
            fg="black",
            font="none 12 bold",
            width=25,
        )
        self.delay_label.grid(row=2, column=0, stick=W)

        self.view_count_label = Label(
            text="Refresh Count:",
            bg="white",
            fg="black",
            font="none 12 bold",
            width=25,
        )
        self.view_count_label.grid(row=3, column=0, stick=W)

        self.link_input = Entry(
            width=50,
        )
        self.link_input.grid(
            row=1,
            column=1,
            sticky=W,
        )

        self.delay_input = Entry(
            width=50,
        )
        self.delay_input.grid(
            row=2,
            column=1,
            sticky=W,
        )

        self.view_count_input = Entry(
            width=50,
        )
        self.view_count_input.grid(
            row=3,
            column=1,
            sticky=W,
        )

        self.start_button = Button(
            text="Start",
            command=self.start,
            width=20,
        )
        self.start_button.grid(
            row=4,
            column=0,
            stick=W,
        )

        self.stop_button = Button(
            text="Stop",
            command=self.stop,
            width=20,
        )
        self.stop_button.grid(
            row=4,
            column=2,
            stick=W,
        )

    def start(self):
        self.url = self.link_input.get().strip()
        self.delay = int(self.delay_input.get())
        self.view_count = int(self.view_count_input.get())
        print(self.url, self.delay, self.view_count)

    def stop(self):
        self.destroy()

    def on_closing(self):
        self.destroy()

def main():
    app = Main()
    app.mainloop()
