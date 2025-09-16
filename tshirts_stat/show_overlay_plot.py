
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from helpers import get_applications, get_accepted_applications, get_confirmed_applications

"""
Estimated:
S-90, M-227, L-168 , XL- 54, XXL - 11
Old: 18, 118, 346, 258, 78, 16
"""

def get_tshirt_size_counts():
    """
    Get t-shirt size counts for all applications, accepted applications, and confirmed applications
    """
    # Use hardcoded estimated values from comment: S-90, M-227, L-168, XL-54, XXL-11
    estimated_counts = {'S': 90, 'M': 227, 'L': 168, 'XL': 54, 'XXL': 11}
    
    # Get accepted applications
    accepted_applications = get_accepted_applications()
    accepted_sizes = []
    for uid, application_data in accepted_applications.items():
        if "hackathon" in application_data and "shirtSize" in application_data["hackathon"]:
            size = application_data["hackathon"]["shirtSize"]
            # Combine XS with S
            if size == "XS":
                size = "S"
            accepted_sizes.append(size)
    
    # Get confirmed applications
    confirmed_applications = get_confirmed_applications()
    confirmed_sizes = []
    for uid, application_data in confirmed_applications.items():
        if "hackathon" in application_data and "shirtSize" in application_data["hackathon"]:
            size = application_data["hackathon"]["shirtSize"]
            # Combine XS with S
            if size == "XS":
                size = "S"
            confirmed_sizes.append(size)
    
    return estimated_counts, accepted_sizes, confirmed_sizes

def create_overlay_plot():
    """
    Create an overlay plot showing t-shirt size distribution for estimated, accepted, and confirmed participants
    """
    estimated_counts, accepted_sizes, confirmed_sizes = get_tshirt_size_counts()
    
    # Count occurrences of each size for accepted and confirmed
    accepted_counts = Counter(accepted_sizes)
    confirmed_counts = Counter(confirmed_sizes)
    
    # Define size order from S to XXL
    size_order = ['S', 'M', 'L', 'XL', 'XXL']
    
    # Get counts for each size in the specified order
    estimated_data = [estimated_counts.get(size, 0) for size in size_order]
    accepted_data = [accepted_counts.get(size, 0) for size in size_order]
    confirmed_data = [confirmed_counts.get(size, 0) for size in size_order]
    
    # Normalize data to proportions
    estimated_total = sum(estimated_data)
    accepted_total = sum(accepted_data)
    confirmed_total = sum(confirmed_data)
    
    estimated_proportions = [(count / estimated_total) if estimated_total > 0 else 0 for count in estimated_data]
    accepted_proportions = [(count / accepted_total) if accepted_total > 0 else 0 for count in accepted_data]
    confirmed_proportions = [(count / confirmed_total) if confirmed_total > 0 else 0 for count in confirmed_data]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = range(len(size_order))
    width = 0.25
    
    # Create bars with offset positions using normalized data
    bars1 = ax.bar([i - width for i in x], estimated_proportions, width, label='Estimated', alpha=0.8, color='lightblue')
    bars2 = ax.bar(x, accepted_proportions, width, label='Accepted', alpha=0.8, color='orange')
    bars3 = ax.bar([i + width for i in x], confirmed_proportions, width, label='Confirmed', alpha=0.8, color='green')
    
    # Customize the plot
    ax.set_xlabel('T-Shirt Size', fontsize=12)
    ax.set_ylabel('Proportion', fontsize=12)
    ax.set_title('T-Shirt Size Distribution (Proportions): Estimated vs Accepted vs Confirmed', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(size_order)
    ax.legend()
    
    # Add value labels on bars (showing proportions and fractions)
    def add_value_labels(bars, actual_counts, total_count, label_type):
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                count = actual_counts[i]
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{height:.3f}\n({count}/{total_count})', ha='center', va='bottom', fontsize=8)
    
    add_value_labels(bars1, estimated_data, estimated_total, 'estimated')
    add_value_labels(bars2, accepted_data, accepted_total, 'accepted')
    add_value_labels(bars3, confirmed_data, confirmed_total, 'confirmed')
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Display the plot
    plt.show()
    
    # Print summary statistics
    print("\n=== T-Shirt Size Distribution Summary ===")
    print(f"Total Estimated (All Applications): {estimated_total}")
    print(f"Total Accepted: {accepted_total}")
    print(f"Total Confirmed: {confirmed_total}")
    
    print("\nSize Breakdown (Raw Counts):")
    for i, size in enumerate(size_order):
        print(f"{size}: Estimated={estimated_data[i]}, Accepted={accepted_data[i]}, Confirmed={confirmed_data[i]}")
    
    print("\nSize Breakdown (Proportions):")
    for i, size in enumerate(size_order):
        print(f"{size}: Estimated={estimated_proportions[i]:.3f}, Accepted={accepted_proportions[i]:.3f}, Confirmed={confirmed_proportions[i]:.3f}")

if __name__ == "__main__":
    create_overlay_plot()