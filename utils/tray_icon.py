from PIL import Image
from utils.file_operations import resource_path
import threading
import time
import sys
import pystray
import globals


def close_app() -> None:
    globals.requested_to_quit = True
    if globals.stats_root is not None:
        globals.stats_root.show_stats_window()
        globals.stats_root.destroy()
    if globals.icon is not None:
        globals.icon.visible = False
        globals.icon.stop()


def setup_icon(_) -> None:
    globals.icon.visible = True
    while globals.icon.visible:
        time.sleep(2)


def init_icon() -> None:
    globals.icon = pystray.Icon("my_icon", Image.open(resource_path("icon.png") if getattr(sys, 'frozen', False)
                                                      else "icon.png"), "Camel Time")
    globals.icon.menu = pystray.Menu(
        pystray.MenuItem("Quit", close_app),
        pystray.MenuItem("Open statistic", globals.stats_root.show_stats_window)
    )

    icon_thread = threading.Thread(target=globals.icon.run, args=(setup_icon,), daemon=True)
    icon_thread.start()
