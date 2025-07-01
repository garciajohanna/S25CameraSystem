import subprocess
import re
from datetime import datetime, timedelta
from collections import deque

# Mac notification function
def mac_notify(title, message):
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"'
    ])

# Regex for HDR trigger
pattern = re.compile(r'Exposure')  # Or: re.compile(r'isHDRCapture:\s*1')

# Log history (with timestamps)
log_buffer = deque()
max_log_age = timedelta(seconds=30)

# Start logcat
print("📸 Listening for HDR capture events...")
proc = subprocess.Popen(["adb", "logcat", "-v", "time"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

try:
    for raw_line in iter(proc.stdout.readline, b''):
        decoded = raw_line.decode("utf-8").strip()

        # Extract timestamp from beginning of the log line
        try:
            ts_str = decoded[:18]  # e.g. '06-07 16:42:53.306'
            timestamp = datetime.strptime(f"2025-{ts_str}", "%Y-%m-%d %H:%M:%S.%f")
        except:
            continue  # Skip malformed lines

        # Maintain sliding log buffer (only last 30s)
        log_buffer.append((timestamp, decoded))
        while log_buffer and log_buffer[0][0] < timestamp - max_log_age:
            log_buffer.popleft()

        # Detect HDR trigger
        if pattern.search(decoded):
            print(f"🔔 HDR Trigger Found: {decoded}")
            mac_notify("HDR Capture Detected!", decoded)

            # Write buffered log to file
            fname = f"hdr_event_{timestamp.strftime('%Y%m%d_%H%M%S')}.log"
            with open(fname, "w") as f:
                for t, line in log_buffer:
                    f.write(f"{line}\n")
            print(f"📁 Saved pre-HDR logs to: {fname}")

except KeyboardInterrupt:
    print("🛑 Stopped by user.")
    proc.terminate()