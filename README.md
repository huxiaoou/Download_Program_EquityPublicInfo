# 爬取国内股票市场公开信息的小程序

## 爬取沪深两市公开交易的程序

+ download_sse: 爬取上海证券交易所，指定交易日期的公开交易信息，参数为
  + 交易日，格式为"YYYYMMDD"
  + 保存目录
+ download_szse: 爬取深圳证券交易所，指定交易日期的公开交易信息，参数为
  + 交易日，格式为"YYYYMMDD"
  + 保存目录

## 爬取沪深两市公开交易的程序

+ download_forbidden_release: 爬取沪深两市指定时间段内的限售股解禁信息，参数为
  + 起始交易日，格式为"YYYYMMDD"
  + 结束交易日（含），格式为"YYYYMMDD"
  + 保存目录
+ 起始交易日必须小于等于结束交易日。
  + 若起始交易日等于结束交易日，则相当于只下载当日数据，保存文件不含有release_date字段，此模式适用于逐日下载。  
  + 若起始交易日小于结束交易日，则相当于下载一段时间内的数据，保存文件含有release_date字段，此模式适用于批量下载历史数据。