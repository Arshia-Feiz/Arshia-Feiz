import matplotlib.pyplot as plt

# Data to visualize
labels = ['Final Portfolio Value', 'Profit/Loss Compared to Buy and Hold']
values = [0, -487930.72]  # The values you provided

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color=['blue', 'red'])

# Add the exact values on top of the bars
for i, v in enumerate(values):
    plt.text(i, v + (abs(v) * 0.05), f'${v:,.2f}', ha='center', fontsize=12)

# Set the title and labels
plt.title('Investment Results Visualization - Model 1', fontsize=16)
plt.ylabel('Value in USD', fontsize=12)
plt.axhline(0, color='black', linewidth=0.5)  # Adding a baseline at 0

# Display the plot
plt.tight_layout()
plt.show()
