import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

BEHAVIOR_OF_INTEREST = "walk"
# path of the data set
file_path = '/Users/siddhantkarmali/Downloads/ACBM_5XFAD_8month.csv'
data = pd.read_csv(file_path)

# Define light and dark hours
light_hours = list(range(8, 21))
dark_hours = list(range(20, 24)) + list(range(0, 8))
total_hours = light_hours + dark_hours

# Identify the nine behaviors
behaviors = ['drink', 'eat', 'groom', 'hang', 'sniff', 'rear', 'rest', 'walk', 'eathand']

for BEHAVIOR_OF_INTEREST in behaviors:

    # We are only looking at Rest:
    unique_mouse_ids = set(data['Mouse ID'])
    unique_mouse_ids = [mouse_ID for mouse_ID in set(data['Mouse ID']) if "5XFAD" in mouse_ID]
    # print(len(unique_mouse_ids))
    print("Unique Mouse IDs:", sorted(unique_mouse_ids))

    Wt_mouse_id = [mouse_ID for mouse_ID in set(data['Mouse ID']) if not "5XFAD" in mouse_ID]
    # print(len(Wt_mouse_id))
    print("Unique Mouse IDs:", sorted(Wt_mouse_id))

    # lista de los ratones dividos
    Hemi_mouse = unique_mouse_ids
    WT_mouse = Wt_mouse_id
    # print(Hemi_mouse)
    # print(WT_mouse)

    time_notebook_hemi_light = {}
    time_notebook_wt_light = {}


    for mouse in Hemi_mouse:
        time_notebook_hemi_light[mouse] = {}
        # addition of the first key of the dictionary; mouse ID
        for hour_index in light_hours:
            time_notebook_hemi_light[mouse][hour_index] = []
            # Second key of the dictionary (0-23 hours)
            for index, row in data.iterrows():
                if row['Mouse ID'] == mouse and row["Hour (0-23)"] == hour_index:
                    # It is checking the column of the mice ID and the hour to annote the amount of secods spent in a behaviuor throughout the 5 days
                    # print(row['rest'])
                    time_notebook_hemi_light[mouse][hour_index].append(row[BEHAVIOR_OF_INTEREST])

    for mouse in WT_mouse:
        time_notebook_wt_light[mouse] = {}
        for hour_index in light_hours:
            time_notebook_wt_light[mouse][hour_index] = []
            for index, row in data.iterrows():
                if row['Mouse ID'] == mouse and row["Hour (0-23)"] == hour_index:
                    # print(row['rest'])
                    time_notebook_wt_light[mouse][hour_index].append(row[BEHAVIOR_OF_INTEREST])

    average_days_hemi_light = {}
    for mouse in Hemi_mouse:
        average_days_hemi_light[mouse] = []
        # first key of the dictionary that will contain each  mouse ID (10)
        for hour in light_hours:
            red = np.mean(time_notebook_hemi_light[mouse][hour])
            # It is calculating the mean of the seconds spent in a specific hour in the range of 5 days
            average_days_hemi_light[mouse].append(red)
    print("Average days (light):", average_days_hemi_light)

    average_days_wt_light = {}
    for mouse in WT_mouse:
        average_days_wt_light[mouse] = []
        for hour in light_hours:
            blue = np.mean(time_notebook_wt_light[mouse][hour])
            average_days_wt_light[mouse].append(blue)
    #print("Average days:", average_days_wt_light)

    print(average_days_hemi_light)
    # 3
    final_averages_hemi_light = []
    # The list of final averages of the 12 hours
    for hour in light_hours:  # light_hours / dark_hours instead of range to analyze the circadian rhythm
        temp_list = []
        # temporary list to store the values of average_days_hemi (mouse ID)(Hour)
        for mouse_ID in average_days_hemi_light:
            temp_list.append(average_days_hemi_light[mouse_ID][hour-8])
        final_averages_hemi_light.append(np.median(temp_list))
        # Using the values stored in temp_list it is calculating the median and storing it
    print(final_averages_hemi_light)

    final_averages_wt_light = []
    for hour in light_hours:

        temp_list = []
        for mouse_ID in average_days_wt_light:
            temp_list.append(average_days_wt_light[mouse_ID][hour-8])
        final_averages_wt_light.append(np.median(temp_list))
    print(final_averages_wt_light)

    # Plotting data

    time_notebook_hemi_dark = {}
    time_notebook_wt_dark = {}
    dark_hour_map = {20:0, 21:1, 22:2, 23:3, 0:4, 1:5, 2:6, 3:7, 4:8, 5:9, 6:10, 7:11, 8:12}

    for mouse in Hemi_mouse:
        time_notebook_hemi_dark[mouse] = {}
        # addition of the first key of the dictionary; mouse ID
        for hour_index in dark_hours:
            time_notebook_hemi_dark[mouse][hour_index] = []
            # Second key of the dictionary (0-23 hours)
            for index, row in data.iterrows():
                if row['Mouse ID'] == mouse and row["Hour (0-23)"] == hour_index:
                    # It is checking the column of the mice ID and the hour to annote the amount of secods spent in a behaviuor throughout the 5 days
                    # print(row['rest'])
                    time_notebook_hemi_dark[mouse][hour_index].append(row[BEHAVIOR_OF_INTEREST])

    for mouse in WT_mouse:
        time_notebook_wt_dark[mouse] = {}
        for hour_index in dark_hours:
            time_notebook_wt_dark[mouse][hour_index] = []
            for index, row in data.iterrows():
                if row['Mouse ID'] == mouse and row["Hour (0-23)"] == hour_index:
                    # print(row['rest'])
                    time_notebook_wt_dark[mouse][hour_index].append(row[BEHAVIOR_OF_INTEREST])

    average_days_hemi_dark = {}
    for mouse in Hemi_mouse:
        average_days_hemi_dark[mouse] = []
        # first key of the dictionary that will contain each  mouse ID (10)
        for hour in dark_hours:
            red = np.mean(time_notebook_hemi_dark[mouse][hour])
            # It is calculating the mean of the seconds spent in a specific hour in the range of 5 days
            average_days_hemi_dark[mouse].append(red)
    print("Average days (dark):", average_days_hemi_dark)

    average_days_wt_dark = {}
    for mouse in WT_mouse:
        average_days_wt_dark[mouse] = []
        for hour in dark_hours:
            blue = np.mean(time_notebook_wt_dark[mouse][hour])
            average_days_wt_dark[mouse].append(blue)
    #print("Average days:", average_days_wt_light)

    print(average_days_hemi_dark)
    # 3
    final_averages_hemi_dark = []
    # The list of final averages of the 12 hours
    for hour in dark_hours:  # light_hours / dark_hours instead of range to analyze the circadian rhythm
        temp_list = []
        # temporary list to store the values of average_days_hemi (mouse ID)(Hour)
        for mouse_ID in average_days_hemi_dark:
            print(hour, dark_hour_map[hour])
            temp_list.append(average_days_hemi_dark[mouse_ID][dark_hour_map[hour]])
        final_averages_hemi_dark.append(np.median(temp_list))
        # Using the values stored in temp_list it is calculating the median and storing it
    print(final_averages_hemi_dark)

    final_averages_wt_dark = []
    for hour in light_hours:

        temp_list = []
        for mouse_ID in average_days_wt_dark:
            temp_list.append(average_days_wt_dark[mouse_ID][dark_hour_map[hour]])
        final_averages_wt_dark.append(np.median(temp_list))
    print(final_averages_wt_dark)


    plt.figure(figsize=(20, 8))
    xpoints = np.array(dark_hours)
    hemi_data = np.array(final_averages_hemi_dark)
    wt_data = np.array(final_averages_wt_dark)
    plt.title(f"Median {BEHAVIOR_OF_INTEREST} across 5 days", fontsize=22)
    plt.xlabel('Hour (0-23)')
    plt.ylabel('Median behavior across population')
    plt.plot(xpoints, hemi_data, color='red', label='Hemi')
    plt.plot(xpoints, wt_data, color='blue', label='WT')
    plt.axvspan(20, 23, color='blue', alpha=0.2)
    plt.axvspan(0, 8, color='blue', alpha=0.2)
    plt.xticks(np.arange(0, 24, 1))
    plt.legend(loc='best', fontsize='x-large')
    plt.show()



'''
PLOTTING LIGHT GRAPHS - PUT BEFORE RUNNING ACROSS LIGHTING GRAPHS
    plt.figure(figsize=(20, 8))
    xpoints = np.array(light_hours)
    hemi_data = np.array(final_averages_hemi_light)
    wt_data = np.array(final_averages_wt_light)
    plt.title(f"Median {BEHAVIOR_OF_INTEREST} across 5 days", fontsize=22)
    plt.xlabel('Hour (0-23)')
    plt.ylabel('Median behavior across population')
    plt.plot(xpoints, hemi_data, color='red', label='Hemi')
    plt.plot(xpoints, wt_data, color='blue', label='WT')
    plt.axvspan(20, 23, color='blue', alpha=0.2)
    plt.axvspan(0, 8, color='blue', alpha=0.2)
    plt.xticks(np.arange(0, 24, 1))
    plt.legend(loc='best', fontsize='x-large')
    plt.show()

'''#std error of means
#std deviation
#95% ci