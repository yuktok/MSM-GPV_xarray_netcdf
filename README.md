# MSM-GPV_xarray_netcdf解凍プログラム
MSMの解答プログラム　wgrib2 と xarrayを利用します。

前提条件
- windows
- anacondaを利用
- 既に必要なgrib2ファイルがダウンロード済み

## step1
- grib2ファイルをnetcdf形式に変換する
    - そのために必要なwgirb2というツールをインストールする。
        - https://ods.n-kishou.co.jp/tech/blog/detail/2869　を参考にして下さい
        - pathの設定に注意
    -　'grib2_decoder.bat'を利用
        - grib2ファイルが入っているフォルダ（入力フォルダ）は指定できるようになっていますが、出力フォルダはbatのコード内で指定して下さい
        '''
        for %%a in ("%folder%\Z__C_RJTD_2021*_FH16-33_grib2.*") do (
        set "filename=%%~na"
        set "extension=%%~xa"

        echo Processing: %%a
        wgrib2 %%a -netcdf "D:\github\transformer\transformer_MEPS\input_netcfd\%%~na.nc
        )
        '''
        この部分で解答ファイルをしています。
        この例では、2021年の16-33時間のGPVデータの全てを解凍しています。(*は任意の文字を表すため)
        ここを自由に変えて下さい


## step2
- xarrayで回答する。
