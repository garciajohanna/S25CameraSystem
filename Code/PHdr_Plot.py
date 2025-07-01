import re
import pandas as pd
import matplotlib.pyplot as plt

# --- Load and parse log file ---
log_path = "LogH.txt"  # Update this path as needed
with open(log_path, "r") as f:
    lines = f.readlines()

# --- Extract key camera parameters ---
pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*?"
    r"g=(?P<gain>[\d.]+),e_t=(?P<et>[\d.]+),Bv=(?P<Bv>[-\d.]+),"
    r"Ev=(?P<Ev>[-\d.]+),PEv=(?P<PEv>[-\d.]+),.*?lux=(?P<lux>\d+),.*?"
    r"drc=(?P<drc>[\d.]+),PHdr=(?P<PHdr>[\d.]+)"
)

data = [m.groupdict() for line in lines if (m := pattern.search(line))]

# --- Create DataFrame ---
df = pd.DataFrame(data)
df = df.astype({
    "gain": float, "et": float, "Bv": float, "Ev": float, "PEv": float,
    "lux": int, "drc": float, "PHdr": float
})
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["Ev_diff"] = df["Ev"].diff()

# --- Identify fusion trigger ---
# df["fusion_event"] = (df["PHdr"] > 0.01) & (df["drc"] > 5) & (df["Ev_diff"] < 0)

# --- Plot PHdr with fusion events ---
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["PHdr"], label="PHdr", color="blue", marker='o')
# plt.scatter(df[df["fusion_event"]]["timestamp"], df[df["fusion_event"]]["PHdr"],
#             color="red", label="Fusion Trigger", zorder=5)
plt.xlabel("Timestamp")
plt.ylabel("PHdr Value")
plt.title("PHdr with HDR Fusion Triggers")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()