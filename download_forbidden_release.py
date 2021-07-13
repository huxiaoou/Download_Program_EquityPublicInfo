from setup import *

report_date = sys.argv[1]

# set headers
exchange_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "referer": "http://www.sse.com.cn/disclosure/diclosure/public/",
}

# download link
rid = int(random.random() * 1e5)
ts = str(int(dt.datetime.timestamp(dt.datetime.now()) * 1000))
download_link = "http://query.sse.com.cn/infodisplay/showTradePublicFile.do?jsonCallBack=jsonpCallback{0:05d}&isPagination=false&dateTx={2}-{3}-{4}&_={1}".format(
    rid, ts, report_date[0:4], report_date[4:6], report_date[6:8]
)

download_link = "http://query.sse.com.cn/infodisplay/showTradePublicFile.do?jsonCallBack=jsonpCallback{0:05d}&isPagination=false&dateTx={2}-{3}-{4}&_={1}".format(
    rid, ts, report_date[0:4], report_date[4:6], report_date[6:8]
)