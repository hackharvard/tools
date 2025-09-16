import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
df = pd.read_csv("csv/tshirts.csv")  # replace with your CSV file path

# Count frequency of sizes
size_counts = df['size'].value_counts()

# Plot histogram (bar chart)
plt.figure(figsize=(8,6))
bars = plt.bar(size_counts.index, size_counts.values)

# Add frequency labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, str(height),
             ha='center', va='bottom', fontsize=10)

# Labels and title
plt.xlabel("Size")
plt.ylabel("Frequency")
plt.title("(Accepted) Frequency of Sizes")
plt.show()

