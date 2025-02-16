import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("results.csv")

# Get the best (smallest) loss per topology
best_loss = df.groupby("Topology")["Loss"].min()

# Plot bar graph
plt.figure(figsize=(8, 5))
best_loss.plot(kind="bar", color=["blue", "green", "red"])
plt.title("Loss Comparison Across Topologies")
plt.ylabel("Smallest Loss Value")
plt.xlabel("Topology")
plt.xticks(rotation=15)
plt.grid(axis="y")

# Save the plot
plt.savefig("figures/best_loss_comparison.png")
plt.show()
