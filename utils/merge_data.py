import requests
import xmltodict
import json
import pandas as pd
import numpy as np
from datetime import datetime as dt

def get_data_by_API(d):
    date = dt.strptime(d, '%Y%m%d')

    url = 'http://openapi.seoul.go.kr:8088/6e4c526d4b63617435304e497a774d/xml/disabledCalltaxi/1/1000/{}'.format(
        date.strftime('%Y%m%d'))

    response = requests.get(url)
    dictionary = xmltodict.parse(response.content)
    json_object = json.dumps(dictionary)
    json_object = json.loads(json_object)

    return json_object

def make_dataset(d):
    date = dt.strptime(d, '%y-%m-%d')
    date_str = date.strftime('%Y%m%d')

    API_data = get_data_by_API(date_str)
    API_df = pd.DataFrame(API_data['openXMLSEOUL']['ROW']['list']['item'])
    provided_df = pd.read_excel('2022.xlsx')

    # API_df 가공
    API_df = API_df.drop(['receipttime'], axis=1)
    cols_1 = ['settime', 'ridetime']
    API_df[cols_1] = API_df[cols_1].apply(lambda x: pd.to_datetime(x.str.replace('오전', 'AM').str.replace('오후', 'PM'), format='%Y-%m-%d %p %I:%M:%S'))
    API_df[cols_1] = API_df[cols_1].apply(lambda x: x.dt.strftime('%Y-%m-%d %H:%M'))

    # provided_df 가공
    provided_df['희망일시'] = pd.to_datetime(provided_df['희망일시'])
    input_date = pd.to_datetime(date_str, format='%Y%m%d')
    provided_df = provided_df[provided_df['희망일시'].dt.date == input_date.date()]

    provided_df = provided_df.dropna(subset=['승차거리'], how='any', axis=0)
    provided_df = provided_df[['접수일시', '희망일시', '배차시간', '탑승시간', '하차시간', '대기시간', '출발구', '출발동', '목적구', '목적동', '승차거리', '요금']]
    provided_df.columns = ['receipttime', 'desiredtime', 'settime', 'ridetime', 'endtime', 'waittime', 'startpos1', 'startpos2', 'endpos1', 'endpos2', 'distance', 'fee']
    cols_2 = ['receipttime', 'desiredtime', 'settime', 'ridetime', 'endtime']
    for col in cols_2:
        provided_df[col] = provided_df[col].apply(pd.to_datetime)
        provided_df = provided_df[provided_df[col].dt.hour >= 7]
    provided_df['traveltime'] = provided_df['endtime'] - provided_df['ridetime']
    provided_df[cols_2] = provided_df[cols_2].apply(lambda x: x.dt.strftime('%Y-%m-%d %H:%M'))

    # API_df와 provided_df merge
    join_df = pd.merge(left=API_df, right=provided_df, how='inner', on=['settime', 'ridetime', 'startpos1', 'startpos2', 'endpos1', 'endpos2'], sort=False)
    join_df = join_df[['no', 'receipttime', 'desiredtime', 'settime', 'ridetime', 'endtime', 'traveltime', 'startpos1', 'startpos2',
       'endpos1', 'endpos2', 'waittime', 'distance', 'fee', 'cartype']]

    # join_df 가공
    join_df[cols_2] = join_df[cols_2].apply(pd.to_datetime)
    for col in cols_2:
        join_df[col] = join_df[col] - pd.to_timedelta(7, unit='h')
        join_df[col] = join_df[col].dt.hour * 60 + join_df[col].dt.minute
    join_df['traveltime'] = join_df['traveltime'].dt.total_seconds() / 60
    join_df['traveltime'] = join_df['traveltime'].astype(int)
    join_df['distance'] = join_df['distance'].astype(int)

    with open('dong_id.json') as f:
        dong_data = json.load(f)
    dong_df = pd.DataFrame(list(dong_data.items()), columns=['startpos2', 'startposid'])
    join_df = pd.merge(join_df, dong_df, on='startpos2', how='left')
    dong_df = pd.DataFrame(list(dong_data.items()), columns=['endpos2', 'endposid'])
    join_df = pd.merge(join_df, dong_df, on='endpos2', how='left')
    join_df = join_df[['no', 'receipttime', 'desiredtime', 'settime', 'ridetime', 'endtime', 'traveltime', 'startposid', 'endposid', 'waittime', 'distance', 'fee']]
    join_df = join_df[np.isfinite(join_df['startposid'])]
    join_df = join_df[np.isfinite(join_df['endposid'])]
    join_df['startposid'] = join_df['startposid'].astype(int)
    join_df['endposid'] = join_df['endposid'].astype(int)
    join_df = join_df[join_df['distance'] != 0]

    join_df['car_marker'] = ''  # Creating a new empty column

    # Unique cars in the DataFrame
    unique_cars = join_df['no'].unique()

    for car in unique_cars:
        # Get the indices of the current car
        indices = join_df[join_df['no'] == car].index
        if (len(indices) == 1):
            join_df.loc[indices[0], 'car_marker'] = 'once'
        else:
            # Mark the first and last appearance of the current car
            join_df.loc[indices[0], 'car_marker'] = 'start'
            join_df.loc[indices[-1], 'car_marker'] = 'end'

    # iterate through df car and if empty fill with "none"
    join_df['car_marker'] = join_df['car_marker'].replace('', 'none')

    join_df.to_csv('output.csv', index=True)