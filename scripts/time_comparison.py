import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("results.csv")

# Get the best (smallest) execution time per topology
best_execution_times = df.groupby("Topology")["Execution Time (s)"].min()

# Plot bar graph
plt.figure(figsize=(8, 5))
best_execution_times.plot(kind="bar", color=["blue", "green", "red"])
plt.title("Time Comparison Across Topologies")
plt.ylabel("Best Execution Time (s)")
plt.xlabel("Topology")
plt.xticks(rotation=15)
plt.grid(axis="y")

# Save the plot
plt.savefig("figures/best_execution_time_comparison.png")
plt.show()
