import xarray as xr
import time

def preprocessing_xr(input_xr):

    start = time.time()
    #日射量のオーダーを合わせる　MJを両方W/m2 kJ/m^2に変換する
    input_xr['DSWRF_surface'] = input_xr['DSWRF_surface']*0.001
    
    #標準化
    val_list = [k for k, v in input_xr.items()]
    for val_col in val_list:
        mean =input_xr[val_col].mean()
        std = input_xr[val_col].std()
        input_xr[val_col] = (input_xr[val_col]-mean.item())/std.item()
    process_time = time.time() - start
    print('前処理完了:時間：{:.3f}s'.format(process_time))

    return input_xr