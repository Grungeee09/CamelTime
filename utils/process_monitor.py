from utils.file_operations import get_data, change_parameter_in_data
from gui.input_dialog import get_name
from gui.ask_yes_or_no import ask_yes_or_no
import psutil
import threading
import time
import datetime
import globals


def check_all_tracked_programs() -> None:
    data = get_data()

    existing_processes: dict = {psutil.Process(pid).name(): pid for pid in psutil.pids()}
    existing_processes_names: set = set(existing_processes.keys())

    for process_name, pid in data["programs"].items():
        if pid is not None and check_process_running(pid):
            on_tracked_app_run(pid, process_name, restart_thread=True)
        elif pid is None and process_name in existing_processes_names:
            on_tracked_app_run(existing_processes[process_name], process_name)
        elif pid is not None and not check_process_running(pid):
            change_parameter_in_data("programs", (process_name, None))


def add_time(pid: int, process_name: str) -> None:
    last_time = datetime.datetime.now()
    while check_process_running(pid) and not globals.requested_to_quit:
        current_time = datetime.datetime.now()
        time_difference = current_time - last_time
        last_time = current_time

        change_parameter_in_data("times", [process_name, round(time_difference.total_seconds(), 2), "+"])

        time.sleep(1)

    if not check_process_running(pid):
        change_parameter_in_data("programs", (process_name, None))


def on_tracked_app_run(pid: int, process_name: str, restart_thread: bool = False) -> None:
    if get_data()["programs"][process_name] is None or restart_thread:
        if not restart_thread:
            change_parameter_in_data("programs", (process_name, pid))
        threading.Thread(target=lambda: add_time(pid, process_name)).start()


def check_process_running(pid) -> bool:
    return psutil.pid_exists(pid)


def on_new_process(process_name: str) -> None:
    answer = ask_yes_or_no("New process", f"Does this process need to be monitored:\n{process_name}?",
                           destroy_after=7.5, font_size=13)

    change_parameter_in_data("runned", process_name)

    if answer:
        display_name = get_name(process_name, "Enter display name:", "Input name")

        change_parameter_in_data("tracked", [process_name, display_name])
        change_parameter_in_data("times", [process_name, 0])
        change_parameter_in_data("programs", (process_name, None))


def check_new_processes() -> None:
    existing_processes = set(psutil.pids())

    while not globals.requested_to_quit:
        new_processes = set(psutil.pids()) - existing_processes
        for pid in new_processes:
            try:
                process = psutil.Process(pid)
                if process.username() != "SYSTEM":
                    if process.name() not in get_data()["runned"]:
                        print("on_new_process", process.name())
                        on_new_process(process.name())
                    if process.name() in get_data()["tracked"]:
                        print("on_tracked_app_run", process.name())
                        on_tracked_app_run(pid, process.name())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        existing_processes = set(psutil.pids())
        time.sleep(0.85)
