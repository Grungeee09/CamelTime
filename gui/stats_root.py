from utils.file_operations import get_data
import globals
import customtkinter as ctk


class StatsRoot(ctk.CTk):
    def __init__(self, debug: float = False) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title(f"Camel Time {globals.__version__}")
        self.geometry("300x300")

        if not debug:
            self.withdraw()

        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.dict_of_programs: dict = {}

        upper_frame = ctk.CTkFrame(self, height=30, fg_color="#242424")
        upper_frame.pack_propagate(False)
        upper_frame.pack(padx=15, pady=(15, 0), fill=ctk.X)

        ctk.CTkButton(upper_frame, text="Update", command=self.update_stats, width=30).pack(side=ctk.LEFT)
        ctk.CTkLabel(upper_frame, text="Top programs by played hours", font=("Arial", 16)).pack(side=ctk.RIGHT)

        self.programs_frame = ctk.CTkScrollableFrame(self, width=230)
        self.programs_frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=10)

        if not globals.requested_to_quit:
            self.update_stats()

    def update_stats(self) -> None:
        self.dict_of_programs = dict(sorted({program_name: {"hours": round(get_data()["times"][process] / 3600, 1),
                                                            "in_game": get_data()["programs"][process] is not None}
                                             for process, program_name in get_data()["tracked"].items()}.items(),
                                            key=lambda item: item[1]["hours"], reverse=True))

        for widget in self.programs_frame.winfo_children():
            widget.destroy()

        for program, other in self.dict_of_programs.items():
            ctk.CTkLabel(self.programs_frame, text=f"{program} - {other["hours"]}h",
                         font=("Arial", 17), text_color="#40a16a" if other["in_game"] else None).pack(pady=4)

    def on_window_close(self) -> None:
        self.withdraw()

    def show_stats_window(self) -> None:
        self.deiconify()
        self.update_stats()
