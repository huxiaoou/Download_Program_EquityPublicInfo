import time

from setup import *

"""
0.  download Public Information from Shenzhen
"""

report_date = sys.argv[1]

# set headers
exchange_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "referer": "http://www.szse.cn/disclosure/deal/public/",
}

for sector_type in ["a", "c"]:
    # download link
    ts = str(int(time.time() * 1000))
    download_link = {
        "a": "http://reportdocs.static.szse.cn/files/text/jy/jy{1}.txt?_={0}".format(ts, report_date[2:]),
        "c": "http://reportdocs.static.szse.cn/files/text/nmTxT/GK/nm_jy{1}.txt?_={0}".format(ts, report_date[2:]),
    }[sector_type]

    # get response
    response = requests.get(url=download_link, headers=exchange_headers)

    # save text
    save_file = "{}.public_info.SZ-{}.txt".format(report_date, sector_type)
    save_path = os.path.join(save_dir, save_file)
    with open(save_path, mode="w+", encoding="utf-8") as f:
        f.write(response.text)

    print("| {} | {} | public info from SZ-{} downloaded |".format(dt.datetime.now(), report_date, sector_type.upper()))
    time.sleep(1)
