import pandas as pd

df = pd.DataFrame()
for i in range(1, 28):
    data = pd.read_csv(f'3func_vhi_id_{i}.csv', index_col=False, header=1)
    data.columns = ['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Unnamed']
    del data['Unnamed']
    data['name'] = str(i)
    data.drop([50], inplace=True)
    data = data[~data.isin([-1])]
    data = data.dropna()
    df = pd.concat([df, data], ignore_index=True)


def min_and_max(df):
    year1 = int(input("enter a year to get min and max: "))
    province1 = input('enter the name of province')
    df1 = df.loc[(df.year == str(year1)) & (df.name == str(province1))]
    print(f"min VHI of {year1} is {df1.VHI.min()}")
    print(f"max VHI of {year1} is {df1.VHI.max()}")
    print(df1)


def extreme_dry(df):
    province1 = input('enter the name of province')
    df1 = df.loc[(df.VHI < 15) & (df.name == str(province1))]
    print(df1.year.unique())


def medium_dry(df):
    province1 = input('enter the name of province')
    df1 = df.loc[(df.VHI > 15) & (df.VHI < 35) & (df.name == str(province1))]
    print(df1.year.unique())


min_and_max(df)
extreme_dry(df)
medium_dry(df)
