import xarray as xr
import time
import glob
from multiprocessing import Pool
#3時間おきの日付を生成するプログラム
from datetime import timedelta
import datetime
def date_range(start, stop, step = timedelta(hours= 3)):
    current = start
    while current < stop:
        yield current
        current += step
    

#https://docs.xarray.dev/en/stable/user-guide/io.html#writing-encoded-data
#https://docs.xarray.dev/en/stable/user-guide/dask.html#dask-io
#こっちでコードした方がよさそう [dask利用]

#データ読み込みのための関数 公式実装
def read_netcdfs(start_date, end_date, dim, netcdf_folder_path, transform_func=None):
    def process_one_path(path):
        # コンテキストマネージャーを使用し、使用後にファイルが閉じられるようにする。
        with xr.open_mfdataset(path, parallel=True) as ds:
            #transform_funcは、何らかの選択または集約を行うべきである。
            if transform_func is not None:
                ds = transform_func(ds)
            # 変換されたデータセットからすべてのデータをロードし，元のファイルを閉じた後にそれを使用できるようにする．
            ds.load()
            return ds

    netcdf_pathlist = []
    for date in date_range(start_date, end_date):
        date = date.strftime('%Y%m%d%H%M%S')
        #一旦24時間後から27時間後までを使うので、16-33時間のデータしか読み込まない
        netcdf_pathlist += glob.glob(netcdf_folder_path+"Z__C_RJTD_{}*_FH16-33_grib2.nc".format(date))

    print(netcdf_pathlist)    
    
    start = time.time()
    datasets = [process_one_path(p) for p in netcdf_pathlist]
    combined = xr.concat(datasets, dim)

    process_time = time.time() - start
    print('読み出し完了：dataset読み込み時間：{:.3f}s'.format(process_time))
    
    return combined




#データ読み込みのための関数
def pdreadxr(path):
    return xr.open_dataset(path).isel(time = slice(8,11))

#multiprocessingを使えば高速化するかもだけど、今のところ出来ない
def readnetcdf_map_multiprocessing(fileslist):
    with Pool() as p:
        output_xr = xr.concat(p.map(pdreadxr, fileslist), dim = 'time')
    return output_xr

def readnetcdf_map_multi(fileslist):
    output_xr = xr.concat(map(pdreadxr, fileslist), dim = 'time')
    return output_xr


def read_netcdf(start_date, end_date ,netcdf_folder_path):
    netcdf_pathlist = []
    for date in date_range(start_date, end_date):
        date = date.strftime('%Y%m%d%H%M%S')
        #一旦24時間後から27時間後までを使うので、16-33時間のデータしか読み込まない
        netcdf_pathlist += glob.glob(netcdf_folder_path+"Z__C_RJTD_{}*_FH16-33_grib2.nc".format(date))
    
    start = time.time()
    output_xr = readnetcdf_map_multiprocessing(netcdf_pathlist)
    process_time = time.time() - start
    print('読み出し完了：dataset読み込み時間：{:.3f}s'.format(process_time))

    return output_xr



