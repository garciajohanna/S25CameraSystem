import re
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURE PATH ===
log_file = "LogH.txt"

# === LOAD FILE ===
with open(log_file, "r") as f:
    lines = f.readlines()

# === PARSE CAMERA METADATA ===
main_pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*?"
    r"g=(?P<gain>[\d.]+),e_t=(?P<et>[\d.]+),Bv=(?P<Bv>[-\d.]+),"
    r"Ev=(?P<Ev>[-\d.]+),PEv=(?P<PEv>[-\d.]+),.*?lux=(?P<lux>\d+),.*?"
    r"drc=(?P<drc>[\d.]+),PHdr=(?P<PHdr>[\d.]+)"
)

evcomp_pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*?EvCompensation\s+[-\d]+->(?P<evcomp>[-\d]+)"
)

main_data = []
evcomp_data = []

for line in lines:
    if (m := main_pattern.search(line)):
        main_data.append(m.groupdict())
    elif (e := evcomp_pattern.search(line)):
        evcomp_data.append({"timestamp": e["timestamp"], "EvComp": int(e["evcomp"])})

# === CREATE MAIN METADATA DATAFRAME ===
df = pd.DataFrame(main_data)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["PHdr"] = df["PHdr"].astype(float)
df["drc"] = df["drc"].astype(float)

# === APPLY EV COMPENSATION ===
if evcomp_data:
    ev_df = pd.DataFrame(evcomp_data)
    ev_df["timestamp"] = pd.to_datetime(ev_df["timestamp"])
    ev_df = ev_df.sort_values("timestamp")

    # Forward fill EvCompensation into main df
    df = df.sort_values("timestamp").merge(ev_df, how="outer").sort_values("timestamp")
    df["EvComp"] = df["EvComp"].ffill()
    df = df[df["PHdr"].notna()]  # Filter back to only main metadata rows
    df = df[df["drc"].notna()]  # Filter back to only main metadata rows

# === PLOT PHdr AND EvComp ===
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(df["timestamp"], df["PHdr"], color="blue", marker="o", label="PHdr")
ax1.set_xlabel("Timestamp")
ax1.set_ylabel("PHdr Value", color="blue")
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)
ax2.plot(df["timestamp"], df["PHdr"], color="blue", marker="o", label="PHdr")
ax2.set_xlabel("Timestamp")
ax2.set_ylabel("PHdr Value", color="blue")
ax2.tick_params(axis='y', labelcolor='blue')

# if "EvComp" in df.columns:
#     ax2 = ax1.twinx()
#     ax2.plot(df["timestamp"], df["EvComp"], color="red", marker="x", linestyle='--', label="Ev Compensation")
#     ax2.set_ylabel("Ev Compensation", color="red")
#     ax2.tick_params(axis='y', labelcolor='red')

fig.suptitle("PHdr and Ev Compensation Over Time")
fig.autofmt_xdate()
plt.tight_layout()
plt.show()