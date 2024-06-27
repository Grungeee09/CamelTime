import customtkinter as ctk


class AskYesOrNoRoot(ctk.CTk):
    def __init__(self, title: str = "Question", text: str = "Some question",
                 font_size: int = 20, destroy_after: int | float = None) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.resizable(False, False)
        self.geometry("290x170")
        self.title(title)

        self.answer: bool = False

        label_frame = ctk.CTkFrame(self, fg_color="#242424")
        label_frame.pack(padx=20, pady=(20, 0), fill=ctk.BOTH, expand=True)

        ctk.CTkLabel(label_frame, text=text, font=("Bold", font_size), anchor="center").pack(expand=True)

        buttons_frame = ctk.CTkFrame(self, fg_color="#242424")
        buttons_frame.pack(padx=15, pady=(40, 20), fill=ctk.X)

        ctk.CTkButton(buttons_frame, text="Yes", width=120, command=self.answer_yes).pack(side=ctk.LEFT)
        ctk.CTkButton(buttons_frame, text="No", width=120, command=self.destroy).pack(side=ctk.RIGHT)

        self.after(int(destroy_after*1000), self.destroy)

        self.mainloop()

    def answer_yes(self) -> None:
        self.answer = True
        self.destroy()

    def get_answer(self) -> bool:
        return self.answer


def ask_yes_or_no(title: str = "Question", text: str = "Some question",
                  font_size: int = 20, destroy_after: int | float = None) -> bool:
    return AskYesOrNoRoot(title, text, font_size, destroy_after).get_answer()
