from analyze import SensitivityData, one_plot

df_list = []
for deg in range(15, 86, 10):
    print(deg)
    if (deg == 15) | (deg == 35):
        pass
    else:
        sensdata = SensitivityData(path='../phantoms/crossing_fibers/results/',
                                   metric='angle',
                                   value=deg)
        sensdata.save_all('by_angle_results/')
        df_list.append(sensdata)

ax = one_plot(df_list, save=True, path='by_angle_results/')
