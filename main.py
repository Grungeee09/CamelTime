from utils.process_monitor import check_all_tracked_programs, check_new_processes
from utils.file_operations import auto_save, check_data_file
from utils.tray_icon import init_icon
from gui.stats_root import StatsRoot
import threading
import globals


def init_program() -> None:
    check_all_tracked_programs()
    init_icon()

    threading.Thread(target=check_new_processes).start()
    threading.Thread(target=lambda: auto_save(1, 3)).start()


def main() -> None:
    check_data_file()
    globals.stats_root = StatsRoot()
    threading.Thread(target=init_program).start()
    globals.stats_root.mainloop()


if __name__ == "__main__":
    main()
