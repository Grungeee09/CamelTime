from typing import Any, Callable
from tkinter.messagebox import showerror
from pathlib import Path
import sys
import globals
import json
import os
import time
import shutil
import datetime


def load_last_save(autosaves_folder: str = "Autosaves") -> None:
    if not getattr(sys, 'frozen', False):
        shutil.copy(f"{autosaves_folder}/{find_save_by_data(autosaves_folder, max)}",
                    os.path.dirname(os.path.abspath(__file__)).removesuffix("utils") + "data.json")
    else:
        with open(f"{autosaves_folder}/{find_save_by_data(autosaves_folder, max)}", "r") as file:
            save: str = file.read()
        with open("data.json", "w") as file:
            file.write(save)


def check_data_file() -> None:
    if not os.path.exists("data.json"):
        create_data_file()
    else:
        try:
            with open("data.json", "r") as file:
                json.load(file)
        except json.decoder.JSONDecodeError:
            if os.path.exists("Autosaves") and os.listdir("Autosaves"):
                load_last_save()
            else:
                os.remove("data.json")
                create_data_file()


def find_save_by_data(folder_path: str, min_or_max: Callable) -> str:
    list_of_saves_paths: list = list(map(lambda x: f"{folder_path}/{x}", os.listdir(folder_path)))
    return min_or_max(list_of_saves_paths, key=os.path.getctime).removeprefix(f"{folder_path}/")


def delete_unnecessary_save(max_file_count: int, folder_path: str = "Autosaves") -> None:
    if len(os.listdir(folder_path)) == max_file_count:
        os.remove(f"{folder_path}/{find_save_by_data(folder_path, min_or_max=min)}")


def save_data(folder_path: str) -> None:
    try:
        shutil.copy("data.json",
                    f"{folder_path}/data_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json")
    except Exception as e:
        showerror(str(e))


def auto_save(delay_min: int | float, max_file_count: int, folder_name: str = "Autosaves") -> None:
    while not globals.requested_to_quit:
        for _ in range(int(delay_min*60*2)):
            if not globals.requested_to_quit:
                time.sleep(0.5)
            else:
                break
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        delete_unnecessary_save(max_file_count, folder_name)
        save_data(folder_name)


def wait_for_file_operations() -> None:
    while globals.wait_for_write_data:
        time.sleep(0.45)

    globals.wait_for_write_data = True


def create_data_file() -> None:
    if not os.path.exists("data.json"):
        json_template = {
            "runned": globals.default_runned_apps,
            "tracked": {},
            "programs": {},
            "times": {}
        }

        wait_for_file_operations()

        with open("data.json", "w") as file:
            json.dump(json_template, file, indent=4)

        globals.wait_for_write_data = False


def get_data() -> dict:
    create_data_file()

    try:
        wait_for_file_operations()

        with open("data.json", "r") as file:
            data = json.load(file)

        globals.wait_for_write_data = False

        return data
    except json.decoder.JSONDecodeError as e:
        print(f"error {e}")


def change_parameter_in_data(parameter: str, new_data: Any) -> None:
    data = get_data()

    if isinstance(data[parameter], (list, set)):
        data[parameter].append(new_data)
    elif isinstance(data[parameter], dict):
        if len(new_data) == 2:
            data[parameter].update({new_data[0]: new_data[1]})
        elif len(new_data) == 3:
            if new_data[2] == "+":
                data[parameter].update({new_data[0]: data[parameter][new_data[0]] + new_data[1]})
    else:
        data[parameter] = new_data

    wait_for_file_operations()

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    globals.wait_for_write_data = False


def resource_path(relative_path):
    """ Get an absolute path to resource, works for a dev and for PyInstaller. """
    # noinspection PyProtectedMember
    return os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath('.'), relative_path)

