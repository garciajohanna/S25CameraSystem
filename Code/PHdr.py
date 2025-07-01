import subprocess
import re
import threading
from datetime import datetime

# Regex for PHdr
pattern = re.compile(r'PHdr=')

# Output file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"logcat_full_{timestamp}.txt"

# Control flag
stop_flag = False

def listen_for_quit():
    global stop_flag
    while True:
        user_input = input("👂 Press 'q' then Enter to stop...\n")
        if user_input.lower().strip() == 'q':
            stop_flag = True
            break

# Start the logcat process
print("📄 Saving full logcat output...")
print("🔎 Highlighting lines containing 'PHdr='")

proc = subprocess.Popen(["adb", "logcat"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# Start the input thread (non-daemon)
input_thread = threading.Thread(target=listen_for_quit)
input_thread.start()

try:
    with open(output_file, 'w') as f:
        while not stop_flag:
            line = proc.stdout.readline()
            if not line:
                break
            decoded = line.decode("utf-8")
            f.write(decoded)
            if pattern.search(decoded):
                print(f"🔍 {decoded.strip()}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    proc.terminate()
    input_thread.join()  # Wait for input thread to finish
    print(f"\n🛑 Stopped. Log saved to: {output_file}")