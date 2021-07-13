import os
import sys
import requests
import datetime as dt
import random
import json

"""
0.  download Public Information from Shanghai
"""


def parse_content_text(t_raw_text: str, t_rid: int):
    j_text = t_raw_text.replace("jsonpCallback{:05d}(".format(t_rid), "{\"content\":")
    j_text = j_text[:-1] + "}"
    d = json.loads(j_text)
    return d["content"]["fileContents"]


report_date = sys.argv[1]
save_dir = sys.argv[2]

# set headers
browser_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "referer": "http://www.sse.com.cn/disclosure/diclosure/public/",
}

# download link
rid = int(random.random() * 1e5)
ts = str(int(dt.datetime.timestamp(dt.datetime.now()) * 1000))
download_link = "http://query.sse.com.cn/infodisplay/showTradePublicFile.do?jsonCallBack=jsonpCallback{0:05d}&isPagination=false&dateTx={2}-{3}-{4}&_={1}".format(
    rid, ts, report_date[0:4], report_date[4:6], report_date[6:8]
)

# get response
response = requests.get(url=download_link, headers=browser_headers)

# parse text
clean_text = parse_content_text(t_raw_text=response.text, t_rid=rid)

# save text
save_file = "{}.public_info.SSE.txt".format(report_date)
save_path = os.path.join(save_dir, save_file)
with open(save_path, mode="w+", encoding="utf-8") as f:
    for line in clean_text:
        f.write(line + "\n")

print("| {} | {} | public info from SH downloaded |".format(dt.datetime.now(), report_date))
