import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
fig, ax = plt.subplots(figsize=(14, 4), dpi=140)
ax.set_axis_off()
fig.patch.set_facecolor("#0f172a")
ax.set_facecolor("#0f172a")
ax.text(0.5, 0.62, "Customer & Product Analytics on 100k Real Orders",
        color="white", fontsize=26, fontweight="bold", ha="center", va="center")
ax.text(0.5, 0.32, "Retention · Funnel · Churn · LTV · Delivery Impact  |  SQL · Python · Streamlit",
        color="#94a3b8", fontsize=14, ha="center", va="center")
plt.savefig(ROOT / "charts" / "banner.png", bbox_inches="tight", facecolor=fig.get_facecolor())
print("banner saved")
