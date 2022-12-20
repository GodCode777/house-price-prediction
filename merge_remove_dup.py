import os
import pandas as pd
import re
import numpy as np

folder = 'houses_links'
files = os.listdir(os.path.join(os.getcwd(), folder))

main_df = pd.DataFrame()

for file in files:
    p = os.path.join(os.getcwd(), folder, file)
    main_df = main_df.append(pd.read_excel(p), ignore_index = True)

main_df.drop([main_df.columns[0]], axis = 1, inplace=True)

main_df['number'] = np.array([int(re.findall('[0-9]+', x)[0]) for x in main_df['houses']])

temp = len(main_df)

main_df.drop_duplicates(subset='number', keep='first', inplace=True)
print(f'Rows removed -> {temp - len(main_df)}')

main_df.drop('number', inplace=True, axis = 1)

main_df.to_excel('main_combined_links.xlsx', index=False)
