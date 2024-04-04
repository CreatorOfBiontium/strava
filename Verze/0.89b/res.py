import os
import sys
import time

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def restart_with_new_script(new_script, mode, target_pid=None):
    try:
        # Získání cesty k aktuálnímu spuštěnému skriptu
        current_script = os.path.abspath(sys.argv[0])

        # Ukončení cílového procesu, pokud je specifikován PID
        if target_pid is not None and mode is not None:
            
            # Mody jsem sem dal pro budoucí využití
            if mode == "restart":
                if os.name == "nt":
                    os.system(f"taskkill /f /pid {target_pid}")
                else:
                    os.system(f"kill -9 {target_pid}")
                time.sleep(2)
            elif mode == "pshdwn":
                if os.name == "nt":
                    os.system(f"taskkill /f /pid {target_pid}")
                else:
                    os.system(f"kill -9 {target_pid}")
                    
                time.sleep(2)
            else:
                print("Modes avalible: restart/pshdwn")
                sys.exit(1)

        # Spuštění nového skriptu
        os.system(f"python {new_script}")

    except Exception as e:
        print(f"Chyba při restartování skriptu: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Syntax Error: call this script by: res.py <new_file.py> <new_file.py pid> <mode>")
        sys.exit(1)

    new_script = sys.argv[1]
    
    target_pid = None
    if len(sys.argv) == 4:
        try:
            target_pid = int(sys.argv[2])
        except ValueError:
            print("Bad PID.")
            sys.exit(1)
            
        try:
            mode = sys.argv[3]
        except:
            print("Plese define a mode, choose from restart/pshdwn")
            sys.exit(1)
            
    restart_with_new_script(new_script, mode, target_pid)
