import torch
import xarray as xr
from datetime import date,timedelta
import pandas as pd
from typing import List, Tuple
import math
import numpy as np

#純粋なslidingwindowでの実装
class TimeSeriesDataSet(torch.utils.data.Dataset):
    def __init__(self, xr : xr.Dataset,  target_df: pd.DataFrame, window_size : int, start_date, end_date) -> None:
        self.xr = xr
        self.window_size = window_size
        self.start_date = start_date
        self.end_date = end_date
        self.target_df = target_df

    def __len__(self) -> int:
        return len(self.target_df)

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:

        target_date = self.target_df['date_UTC'].iloc[idx]
        target = self.target_df['solar irrdance'].iloc[idx]
        # sliding window 予測時間から　window_size時間前　の値から読み出す
        ##window_size時間前にデータがあるのか精査しないとダメ！！！(未実装)
        X_xr = self.xr.sel(time = slice(target_date - timedelta(hours = self.window_size -1 ) , target_date))

        #tensor化
        X_xr_tensor = torch.tensor(X_xr.to_array().transpose('time','variable' ,'latitude', 'longitude').to_numpy())
        target_tensor = torch.tensor(target)
        return X_xr_tensor, target_tensor
    

class Table_TimeSeriesDataSet(torch.utils.data.Dataset):
    def __init__(self, xr : xr.Dataset,  target_df: pd.DataFrame, window_size : int, start_date, end_date) -> None:
        self.xr = xr
        self.window_size = window_size
        self.start_date = start_date
        self.end_date = end_date
        self.target_df = target_df
        self.target_df.iloc[:,'Sin_hour'] = np.sin(self.target_df['hour']/24*2*np.pi)

    def __len__(self) -> int:
        return len(self.target_df)

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:

        target_date = self.target_df['date_UTC'].iloc[idx]
        target = self.target_df['solar irrdance'].iloc[idx]   
        # sliding window 予測時間から　window_size時間前　の値から読み出す
        ##window_size時間前にデータがあるのか精査しないとダメ！！！(未実装)
        X_xr = self.xr.sel(time = slice(target_date - timedelta(hours = self.window_size -1 ) , target_date))

        #tensor化
        X_xr_tensor = torch.tensor(X_xr.to_array().transpose('time','variable' ,'latitude', 'longitude').to_numpy())
        target_tensor = torch.tensor(target)

        table_data = torch.tensor(self.target_df[['Downward short-wave radiation flux','Sin_hour']].iloc[idx].to_numpy(), dtype=torch.float32)
        
        '''
        table_data = torch.tensor(self.target_df[['Pressure reduced to MSL', 'Pressure',
       'u-component of wind', 'v-component of wind', 'Temperature',
       'Relative humidity', 'Low cloud cover', 'Medium cloud cover',
       'High cloud cover', 'Total cloud cover', 'Total precipitation',
       'Downward short-wave radiation flux', 'sun altitude']].iloc[idx].to_numpy(), dtype=torch.float32)
       '''
        return X_xr_tensor, target_tensor , table_data