from analyze import SensitivityData, one_plot
import matplotlib.pyplot as plt

df_list = []
for r in [4, 8, 12, 16]:
    print(r)
    sensdata = SensitivityData(path='../phantoms/different_size/results/',
                               metric='radius',
                               value=r)
    sensdata.save_all('by_size_results/')
    df_list.append(sensdata)

ax = one_plot(df_list, save=True, path='by_size_results/')
