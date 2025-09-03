import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------
# Settings
# -----------------------------------
folder_path = r"C:\Users\L136_L2\Documents\8262026"  # <-- change if needed
x_min = -0.0534375e-7
x_max = 1.0e-8
SCALE = 1e10

# -----------------------------------
# Helper: extract number after "pol2_"
# -----------------------------------
def extract_pol2_number(stem):
    match = re.search(r'Pol2_(\d+)', stem, re.IGNORECASE)
    if match:
        return match.group(1)  # just the digits after "pol2_"
    return stem  # fallback to full stem if no match

# -----------------------------------
# Read data from all CSVs
# -----------------------------------
csv_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.csv')])
if not csv_files:
    raise FileNotFoundError("No .csv files found in the specified folder.")

data_by_label = {}   # label -> (x, y)
file_info = []       # rows with filename + label

for file in csv_files:
    path = os.path.join(folder_path, file)
    df = pd.read_csv(path)

    # Convert first two columns to numeric and drop bad rows
    x_raw = pd.to_numeric(df.iloc[:, 0], errors='coerce').to_numpy()
    y_raw = pd.to_numeric(df.iloc[:, 1], errors='coerce').to_numpy()
    valid = ~(np.isnan(x_raw) | np.isnan(y_raw))
    x = x_raw[valid]
    y = y_raw[valid]

    stem = os.path.splitext(file)[0]
    label = extract_pol2_number(stem)  # <-- label is number after pol2_

    data_by_label[label] = (x, y)
    file_info.append({"filename": file, "label": label})

# -----------------------------------
# Integrate EACH file separately
# -----------------------------------
rows = []
for row in file_info:
    label = row["label"]
    x, y = data_by_label[label]

    rng_mask = (x >= x_min) & (x <= x_max)
    x_seg = x[rng_mask]
    y_seg = y[rng_mask]

    if x_seg.size >= 2:
        val = np.trapz(np.abs(y_seg), x_seg) * SCALE
    else:
        val = np.nan  # not enough points

    rows.append({
        "filename": row["filename"],
        "label": label,
        "n_points": int(x_seg.size),
        "integral_scaled_1e10": val
    })

results_df = pd.DataFrame(rows)

with pd.option_context('display.float_format', '{:.3e}'.format):
    print("\nIntegration results (absolute, scaled by 1E10):")
    print(results_df)

# -----------------------------------
# Plot with shaded integration regions
# -----------------------------------
plt.figure(figsize=(8, 6))
for row in file_info:
    label = row["label"]
    x, y = data_by_label[label]
    plt.plot(x, y, label=label)

    mask = (x >= x_min) & (x <= x_max)
    if mask.any():
        plt.fill_between(x[mask], y[mask], alpha=0.3)

plt.xlabel("x values")
plt.ylabel("y values")
plt.title("CSV Data with Shaded Integrated Region")
plt.legend(title="pol2_ number")
plt.grid(True)
plt.xlim(x_min, x_max)
plt.tight_layout()
plt.show()

# -----------------------------------
# Polarization plot of integrals
# -----------------------------------
# Convert labels to numeric (angles in degrees)
results_df["angle_deg"] = pd.to_numeric(results_df["label"], errors="coerce")

# Drop rows where label was not a number
results_clean = results_df.dropna(subset=["angle_deg", "integral_scaled_1e10"])

# Convert degrees to radians for polar plot
angles_rad = np.deg2rad(results_clean["angle_deg"].to_numpy())
values = results_clean["integral_scaled_1e10"].to_numpy()

plt.figure(figsize=(6, 6))
ax = plt.subplot(111, polar=True)
ax.plot(angles_rad*2, values, marker="o", linestyle="-", label="Integrated Intensity")
ax.fill(angles_rad*2, values, alpha=0.3)

ax.set_title("Polarization Plot of Integrated Values", va="bottom")
ax.legend(loc="upper right")
plt.show()