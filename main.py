import ctypes
import sys
import winreg
import os

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()


def read_registry_key(key_path, value_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        value, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return None

def write_registry_key(key_path, value_name, new_value):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error writing registry key: {e}")
        return False

key_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
value_name = "ProcessorNameString"

cpu_name = read_registry_key(key_path, value_name)
if cpu_name:
    print(f"Current CPU name: {cpu_name}")
else:
    print("Unable to read CPU name from the registry.")

if not os.path.exists('old'):
    with open('old', 'a') as f:
        f.write(cpu_name)
else:
    old_cpu = open('old', 'r').read()
    ask = input(f"You want to set default to [{old_cpu}] (y/n): ")
    if ask in ['y', 'yes' 'ye']:
        write_registry_key(key_path, value_name, old_cpu)
        os._exit(0)
    else:
        pass
new_cpu_name = input("New Cpu Name: ")
write_registry_key(key_path, value_name, new_cpu_name)