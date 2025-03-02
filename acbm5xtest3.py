import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BEHAVIOR_OF_INTEREST = "groom"
# path of the data set
file_path = '/Users/claudiatoledomolinary/OneDrive - University of Puerto Rico/Brown - Summer 2024/ACBM_5XFAD_8month.csv'

# load excel file
data = pd.read_csv(file_path)
print(data)

# print data - manera de comprobar que había conectado correctamente and it worked
# print(data)

# Define light and dark hours
light_hours = list(range(8, 21))
dark_hours = list(range(21, 24)) + list(range(0, 8))
total_hours = light_hours + dark_hours

# Identify the nine behaviors
behaviors = ['drink', 'eat', 'groom', 'hang', 'sniff', 'rear', 'rest', 'walk', 'eathand']

for BEHAVIOR_OF_INTEREST in behaviors:

    '''
    Esto es una lista (creo) 
    it calls los números de las columnas del data set


    # Initialize dictionaries to store total and count for light and dark hours
    # light_totals = {behavior: 0 for behavior in behaviors}
    # dark_totals = {behavior: 0 for behavior in behaviors}
    # light_counts = {behavior: 0 for behavior in behaviors}
    # dark_counts = {behavior: 0 for behavior in behaviors}


    Los diccionarios guardan números del data set 
    de la manera en que tu quieras. 
    Es decir, estoy clasificando mis datos en 
    light and dark so ya el range estará en función.

    OJO:

    diferencia entre totals y count es:
    totals es el total de veces que ocurrió el behavior 
    mientras que counts es la sumatoria de los segundos por hora que el behavior se llevo a cabo 


    totals = data[behaviors].mean() #hello?????


    so es como un loop pero acaba cuando acaban las columnas
    va una a una hasta que acaba y tengo 9 means 


    # We are going to do everything in this loop one time for each behavior
    #for behavior in behaviors:
    # Average across 5 days of data for each mouse
    '''
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

    time_notebook_hemi = {}
    time_notebook_wt = {}

    # for hour_index in range(0,24):
    #     time_notebook[hour_index] = [] #helloooo?

    # print(time_notebook)

    # Now we are only working with Rest
    # We need to go through the rows of the dataframe, and look for Mouse SID and the Hour
    # hour_of_interest = 1 # i need to create a range?
    # mouse_of_interest = '5XFAD_1398'

    # Hemi_mouse is a list of 5XFAD mice
    # WT_mouse is a list of Wild type mice
    for mouse in Hemi_mouse:
        time_notebook_hemi[mouse] = {}
        # addition of the first key of the dictionary; mouse ID
        for hour_index in range(0, 24):
            time_notebook_hemi[mouse][hour_index] = []
            # Second key of the dictionary (0-23 hours)
            for index, row in data.iterrows():
                if row['Mouse ID'] == mouse and row["Hour (0-23)"] == hour_index:
                    # It is checking the column of the mice ID and the hour to annote the amount of secods spent in a behaviuor throughout the 5 days
                    # print(row['rest'])
                    time_notebook_hemi[mouse][hour_index].append(row[BEHAVIOR_OF_INTEREST])

    for mouse in WT_mouse:
        time_notebook_wt[mouse] = {}
        for hour_index in range(0, 24):
            time_notebook_wt[mouse][hour_index] = []
            for index, row in data.iterrows():
                if row['Mouse ID'] == mouse and row["Hour (0-23)"] == hour_index:
                    # print(row['rest'])
                    time_notebook_wt[mouse][hour_index].append(row[BEHAVIOR_OF_INTEREST])

    # for thayer_street in time_notebook["5XFAD_1407"][0]:
    #     print(thayer_street)

    # print("New Time Notebook:", time_notebook_hemi)
    #
    # print("This is what we have in Time Notebook:",time_notebook)

    # print("Mean time of 'Hour (0-23)':", np.mean(time_notebook[hour_index]))

    # for hour_index in range(0,24):
    #     np.mean(time_notebook[0, 24])
    # print("Mean time of Hour 1:", np.mean(time_notebook[0,24]))

    # #Initiating sum
    # total = 0
    # #
    # average_days = []
    # for hour in range(0,24):
    #     average_numpy = np.mean(time_notebook["5XFAD_1398"][hour])
    #     average_days.append(average_numpy)
    # print("Average Days: ", average_days)
    # 2
    average_days_hemi = {}
    for mouse in Hemi_mouse:
        average_days_hemi[mouse] = []
        # first key of the dictionary that will contain each  mouse ID (10)
        for hour in range(0, 24):
            red = np.mean(time_notebook_hemi[mouse][hour])
            # It is calculating the mean of the seconds spent in a specific hour in the range of 5 days
            average_days_hemi[mouse].append(red)
    print("Average days:", average_days_hemi)

    average_days_wt = {}
    for mouse in WT_mouse:
        average_days_wt[mouse] = []
        for hour in range(0, 24):
            blue = np.mean(time_notebook_wt[mouse][hour])
            average_days_wt[mouse].append(blue)
    print("Average days:", average_days_wt)

    # 3
    final_averages_hemi = []
    # The list of final averages of the 24 hours
    for hour in total_hours:  # light_hours / dark_hours instead of range to analyze the circadian rhythm
        temp_list = []
        # temporary list to store the values of average_days_hemi (mouse ID)(Hour)
        for mouse_ID in average_days_hemi:
            temp_list.append(average_days_hemi[mouse_ID][hour])
        final_averages_hemi.append(np.median(temp_list))
        # Using the values stored in temp_list it is calculating the median and storing it
    print(final_averages_hemi)

    final_averages_wt = []
    for hour in range(0, 24):

        temp_list = []
        for mouse_ID in average_days_wt:
            temp_list.append(average_days_wt[mouse_ID][hour])
        final_averages_wt.append(np.median(temp_list))
    print(final_averages_wt)

    # Plotting data

    plt.figure(figsize=(20, 8))
    xpoints = np.array(light_hours)
    hemi_data = np.array(final_averages_hemi)
    wt_data = np.array(final_averages_wt)
    plt.title(f"Median {BEHAVIOR_OF_INTEREST} across 5 days", fontsize=22)
    plt.xlabel('Hour (0-23)')
    plt.ylabel('Median behavior across population')
    plt.plot(xpoints, hemi_data, color='red', label='Hemi')
    plt.plot(xpoints, wt_data, color='blue', label='WT')
    plt.axvspan(20, 23, color='blue', alpha=0.2)
    plt.axvspan(0, 8, color='blue', alpha=0.2)
    plt.xticks(np.arange(0, 24, 1))
    plt.legend(loc='best', fontsize='x-large')
    plt.savefig(
        f"/Users/claudiatoledomolinary/OneDrive - University of Puerto Rico/Brown - Summer 2024/Graphs8 LD/{BEHAVIOR_OF_INTEREST}_median.png")
    plt.show()
