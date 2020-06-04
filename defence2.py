from spyre import server
import pandas as pd

provinces = {1: 'Черкаська', 2: 'Чернігівська', 3: 'Чернівецька', 4: 'Республіка Крим', 5: 'Дніпропетровська',
             6: 'Донецька', 7: 'Івано-Франківська', 8: 'Харківська', 9: 'Херсонська', 10: 'Хмельницька', 11: 'Київська',
             12: 'місто Київ', 13: 'Кіровоградська', 14: 'Луганська', 15: 'Львівська', 16: 'Миколаївська',
             17: 'Одеська',
             18: 'Полтавська', 19: 'Рівненська', 20: 'місто Севастополь', 21: 'Сумська', 22: 'Тернопільська',
             23: 'Закарпатська', 24: 'Вінницька', 25: 'Волинська', 26: 'Запорізька', 27: 'Житомирська'}

df = pd.DataFrame()
for i in range(1, 28):
    data = pd.read_csv(f'3func_vhi_id_{i}.csv', index_col=False, header=1)
    data.columns = ['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Unnamed']
    del data['SMN']
    del data['SMT']
    del data['Unnamed']
    data['name'] = str(i)
    data.drop([50], inplace=True)
    data = data[~data.isin([-1])]
    data = data.dropna()
    df = pd.concat([df, data], ignore_index=True)


class SecondLAb(server.App):
    title = "Data analysis"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Time series',
            "options": [{"label": "VHI", "value": "VHI"},
                        {"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"}],
            "key": 'timeseries',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Province',
            "options": [{"label": id, "value": name} for name, id in provinces.items()],
            "key": 'province',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'From year',
            "options": [{"label": i, "value": i} for i in range(1982, 2020)],
            "key": 'from_year',
            "action_id": "refresh"
        },
        {
            "type": 'dropdown',
            "label": 'To year',
            "options": [{"label": i, "value": i} for i in range(1982, 2020)],
            "key": 'to_year',
            "action_id": "refresh"
        }
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "table",
            "id": "world",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },
        {"type": "plot",
         "id": "planet",
         "control_id": "update_data",
         "tab": "Plot",
         }]

    def world(self, params):
        time_series = str(params['timeseries'])
        province_num = int(params['province'])
        from_year = int(params['from_year'])
        to_year = int(params['to_year'])
        df1 = pd.DataFrame()
        for i in range(from_year, to_year + 1):
            df2 = df.loc[(df.year == str(i)) & (df.name == str(province_num))]
            df1 = pd.concat([df1, df2], ignore_index=True)

        return df1

    def planet(self, params):
        datatype = params['timeseries']

        plt_obj = self.getData(params).plot(x='year', y=datatype)
        plt_obj.set_ylabel(datatype)
        fig = plt_obj.get_figure()
        return fig


print(df)
app = SecondLAb()
app.launch(port=9094)
