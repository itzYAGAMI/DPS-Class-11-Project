import os
import time
import ctypes
import json
from datetime import datetime

hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
redirect = "127.0.0.1"
saved_settings_file = "block_settings.json"

def save_settings(settings):
    with open(saved_settings_file, "w") as file:
        json.dump(settings, file)

def load_settings():
    try:
        with open(saved_settings_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def block_websites(websites, end_time):
    print(f"Blocking websites: {websites}")
    while datetime.now() < end_time:
        with open(hosts_path, "r+") as file:
            content = file.read()
            for website in websites:
                if website not in content:
                    file.write(f"{redirect} {website}\n")
        time.sleep(5)
    unblock_websites(websites)

def unblock_websites(websites):
    print("Unblocking websites...")
    with open(hosts_path, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(website in line for website in websites):
                file.write(line)
        file.truncate()

def ultra_focus_mode(end_time):
    print("Ultra Focus Mode activated. Task Manager disabled.")
    ctypes.windll.user32.BlockInput(True)
    try:
        while datetime.now() < end_time:
            time.sleep(10)
    finally:
        ctypes.windll.user32.BlockInput(False)
        print("Ultra Focus Mode deactivated.")

def pomodoro_mode(cycles):
    work_duration = 25 * 60
    break_duration = 5 * 60
    for _ in range(cycles):
        print("Focus time! Work for 25 minutes.")
        time.sleep(work_duration)
        print("Break time! Relax for 5 minutes.")
        time.sleep(break_duration)
    print("Pomodoro session complete!")

def absolute_zero_distractions(end_time):
    print("Absolute 0 Distractions Mode activated. Locking screen continuously.")
    while datetime.now() < end_time:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        time.sleep(5)

def main():
    saved_settings = load_settings()
    print("Distraction Blocker")
    print("1. Basic Mode")
    print("2. Ultra Focus Mode")
    print("3. Pomodoro Mode")
    print("4. Absolute 0 Distractions Mode")
    print("5. Manage Saved Settings")

    choice = input("Choose a mode (1-5): ")

    if choice == "1":
        print("Saved settings:")
        for idx, setting in enumerate(saved_settings, start=1):
            print(f"{idx}. {setting}: {saved_settings[setting]}")
        
        setting_choice = input("Choose a saved setting or type 'new' to create one: ")
        if setting_choice.isdigit() and int(setting_choice) <= len(saved_settings):
            websites = saved_settings[list(saved_settings.keys())[int(setting_choice) - 1]]
        else:
            websites = input("Enter websites to block (comma-separated): ").split(",")
            name = input("Enter a name for this setting: ")
            saved_settings[name] = websites
            save_settings(saved_settings)

        duration = int(input("Enter block duration in minutes: "))
        end_time = datetime.now() + timedelta(minutes=duration)
        block_websites(websites, end_time)

    elif choice == "2":
        duration = int(input("Enter block duration in minutes: "))
        end_time = datetime.now() + timedelta(minutes=duration)
        ultra_focus_mode(end_time)

    elif choice == "3":
        cycles = int(input("Enter number of Pomodoro cycles: "))
        pomodoro_mode(cycles)

    elif choice == "4":
        duration = int(input("Enter block duration in minutes: "))
        end_time = datetime.now() + timedelta(minutes=duration)
        absolute_zero_distractions(end_time)

    elif choice == "5":
        print("Saved settings:")
        for idx, setting in enumerate(saved_settings, start=1):
            print(f"{idx}. {setting}: {saved_settings[setting]}")

        manage_choice = input("Type 'delete' to remove a setting or 'back' to return: ")
        if manage_choice == "delete":
            delete_choice = int(input("Enter the number of the setting to delete: "))
            if delete_choice <= len(saved_settings):
                del saved_settings[list(saved_settings.keys())[delete_choice - 1]]
                save_settings(saved_settings)
                print("Setting deleted.")

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
