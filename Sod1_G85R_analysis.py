import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Read the CSV file
df = pd.read_csv('/Users/siddhantkarmali/Downloads/ACBM_5XFAD_2month.csv')

# List of behaviors
behaviors = ['drink', 'eat', 'groom', 'hang', 'sniff', 'rear', 'rest', 'walk', 'eathand']

# Define day, night, and all hours
day_hours = list(range(8, 20)) #lights on
night_hours = list(range(20, 24)) + list(range(0, 8)) #lights off
all_hours = list(range(24))


def calculate_mouse_averages(df, behaviors, hours, time_label):
    # Filter data for the specified hours
    df_filtered = df[df['Hour (0-23)'].isin(hours)]

    # Group by Mouse ID and calculate mean for each behavior
    mouse_averages = df_filtered.groupby('Mouse ID')[behaviors].mean() / 3600  # Convert seconds to hours

    # Add a column for the time period (e.g., "Lights Off")
    mouse_averages['Time Period'] = time_label

    # Reset index to make Mouse ID a column
    mouse_averages = mouse_averages.reset_index()

    return mouse_averages
# Function to plot graphs for given hours with t-tests and p-values
def plot_behavior_with_ttests(df, hours, time_label):
    # Filter data for the specified hours
    df_filtered = df[df['Hour (0-23)'].isin(hours)]

    # Separate 5XFAD and Wild-Type data
    df_5xfad = df_filtered[df_filtered['Genotype'] == 'Hemi']
    df_wt = df_filtered[df_filtered['Genotype'] == 'WT']

    df_5xfad_lon = df_5xfad[df_5xfad['Hour (0-23)'].isin(day_hours)]
    print(df_5xfad_lon)
    df_5xfad_loff = df_5xfad[df_5xfad['Hour (0-23)'].isin(night_hours)]
    print(df_5xfad_loff)

    df_wt_lon = df_wt[df_wt['Hour (0-23)'].isin(day_hours)]
    df_wt_loff = df_wt[df_wt['Hour (0-23)'].isin(night_hours)]

    print("pick up the phone")

    #get means for each mouse
    mean_per_mouse = df.groupby(['Mouse ID', 'Genotype'])[behaviors].mean()
    mean_time_per_mouse_hours = mean_per_mouse / 3600
    mean_time_per_mouse = mean_time_per_mouse_hours.reset_index()
    print(mean_time_per_mouse)



    # Calculate mean time spent on each behavior for 5XFAD and Wild-Type mice
    avg_times_5xfad_t = df_5xfad[behaviors].mean() / 3600  # Convert seconds to hours
    avg_times_5xfad_lon = df_5xfad_lon[behaviors].mean() / 3600
    avg_times_5xfad_loff = df_5xfad_loff[behaviors].mean() / 3600
    #avg_times_5xfad_lon = df_5xfad[behaviors].std() / 3600
    avg_times_wt_t = df_wt[behaviors].mean() / 3600        # Convert seconds to hours
    avg_times_wt_lon = df_wt_lon[behaviors].mean() / 3600
    avg_times_wt_loff = df_wt_loff[behaviors].mean() / 3600


    # print(avg_times_5xfad_t)
    # print(avg_times_5xfad_lon)
    # print(avg_times_5xfad_loff)
    # print(avg_times_wt_t)
    # print(avg_times_wt_lon)
    # print(avg_times_wt_loff)

    print("no diddy")

    # Perform t-tests for each behavior
    p_values = []
    for behavior in behaviors:
        t_stat, p_val = stats.ttest_ind(df_5xfad[behavior], df_wt[behavior], equal_var=False)
        p_values.append(p_val)

    sns.set_style("darkgrid")
    sns.set_palette("deep")
    # Create the plot
    fig, ax = plt.subplots(figsize=(17, 10))

    #make a second y-axis to represent the averages

    ax2 = ax.twinx()



    # Set x-axis positions for the bars
    x = np.arange(len(behaviors))
    width = 0.35

    ax.set_ylim(0, 1)

    # Plot bars for 5XFAD and Wild-Type side by side
    bars_5xfad = ax.bar(x + width/2, avg_times_5xfad_t, width, label='5XFAD', color='steelblue', alpha=0.8)
    bars_wt = ax.bar(x - width/2, avg_times_wt_t, width, label='Wild-Type', color='darkred', alpha=0.8)

    # Add average values above each bar and significance levels
    for i, bar in enumerate(bars_5xfad):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/3., height + 0.05,
                f'{height:.2f}', ha='center', va='bottom', fontsize=8)
        # Display p-values or "ns"
        if p_values[i] < 0.05:
            ax.text(bar.get_x() + bar.get_width()/4., height + 0.1,
                    f'p={p_values[i]:.3f}', ha='center', va='bottom', fontsize=8)
        else:
            ax.text(bar.get_x() + bar.get_width()/5., height + 0.05,
                    'ns', ha='center', va='bottom', fontsize=8)

    for i, bar in enumerate(bars_wt):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/5., height + 0.05,
                f'{height:.2f}', ha='center', va='bottom', fontsize=8)

    # Add a horizontal line at y=0 for reference (optional)
    #ax.axhline(y=0, color='black', linestyle='--')

    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Set labels and title
    ax.set_xlabel('Behaviors', fontsize=12)
    ax.set_ylabel('Standardized Mean Time Spent on Behavior (s/hr)', fontsize=12)
    ax.set_title(f'Average Time Spent on Behaviors ({time_label} - 2-mo 5XFAD vs Wild-Type)', fontsize=16, fontweight='bold')

    # Set x-axis ticks
    ax.set_xticks(x)
    ax.set_xticklabels(behaviors, rotation=45, ha='right')

    # Add legend
    plt.legend(fontsize=10)

    # Adjust layout and display the plot
    plt.tight_layout()

    plt.show()
# Plot for day, night, and all hours separately with t-tests and p-values
plot_behavior_with_ttests(df, day_hours, "Lights On")
plot_behavior_with_ttests(df, night_hours, "Lights Off")
plot_behavior_with_ttests(df, all_hours, "All Hours")