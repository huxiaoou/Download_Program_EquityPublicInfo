import os
import sys
import requests
import datetime as dt
import json
import pandas as pd

pd.set_option("display.width", 0)


def parse_content_text(t_raw_text: str, t_rid: int, t_ts):
    j_text = t_raw_text.replace("jQuery{}_{}(".format(t_rid, t_ts), "{\"content\":")
    j_text = j_text[:-2] + "}"
    d = json.loads(j_text)
    return d["content"]["result"]["data"]


bgn_date = sys.argv[1]
end_date = sys.argv[2]
bgn_date_d10 = bgn_date[0:4] + "-" + bgn_date[4:6] + "-" + bgn_date[6:8]
end_date_d10 = end_date[0:4] + "-" + end_date[4:6] + "-" + end_date[6:8]
save_dir = sys.argv[3]
page_size = 1000

# set headers
browser_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    "referer": "https://data.eastmoney.com/",
}

# download link
rid = 1123006025078678499485
ts = str(int(dt.datetime.timestamp(dt.datetime.now()) * 1000))

cmd_dict = {
    "cmd_str_query": "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery{}_{}".format(rid, ts),
    "cmd_str_sort_col": "&sortColumns=FREE_DATE%2CCURRENT_FREE_SHARES",
    "cmd_str_sort_type": "&sortTypes=1%2C1",
    "cmd_str_page_size": "&pageSize=".format(page_size),
    "cmd_str_page_number": "&pageNumber=1",
    "cmd_str_report_name": "&reportName=RPT_LIFT_STAGE",
    "cmd_str_columns": "&columns={}%2{}%2{}%2{}%2{}%2{}%2{}%2{}%2{}%2{}%2{}%2{}%2{}%2{}".format(
        "SECURITY_CODE",
        "CSECURITY_NAME_ABBR",
        "CFREE_DATE",
        "CCURRENT_FREE_SHARES",
        "CABLE_FREE_SHARES",
        "CLIFT_MARKET_CAP",
        "CFREE_RATIO",
        "CNEW",
        "CB20_ADJCHRATE",
        "CA20_ADJCHRATE",
        "CFREE_SHARES_TYPE",
        "CTOTAL_RATIO",
        "CNON_FREE_SHARES",
        "CBATCH_HOLDER_NUM",
    ),
    "cmd_str_source": "&source=WEB",
    "cmd_str_client": "&client=WEB",
    "cmd_str_filter": "&filter=(FREE_DATE%3E%3D%27{0}%27)(FREE_DATE%3C%3D%27{1}%27)".format(bgn_date_d10, end_date_d10)
}

download_link = "".join(cmd_dict.values())

# get response
response = requests.get(url=download_link, headers=browser_headers)
res = parse_content_text(t_raw_text=response.text, t_rid=rid, t_ts=ts)
df = pd.DataFrame(res)
df["wind_code"] = df["SECURITY_CODE"].map(lambda z: z + (".SH" if z[0:2] in ["60", "68"] else ".SZ"))
rename_mapper = {
    "SECURITY_NAME_ABBR": "chs_name",
    "FREE_DATE": "release_date",
    "ABLE_FREE_SHARES": "release_qty",
    "CURRENT_FREE_SHARES": "release_qty_fact",
    "FREE_RATIO": "prop_to_existing",
    "FREE_SHARES_TYPE": "release_type",
    "NON_FREE_SHARES": "non_free_shares",
}
df = df.rename(mapper=rename_mapper, axis=1).set_index("wind_code")
df["release_date"] = df["release_date"].map(lambda z: z[0:4] + z[5:7] + z[8:10])
df["prop_to_existing"] = df["prop_to_existing"] * 100
df = df[rename_mapper.values()]

if bgn_date != end_date:
    save_file = "forbidden_release.{}.{}.csv.gz".format(bgn_date, end_date)
else:
    save_file = "forbidden_release.{}.csv.gz".format(bgn_date)
    df = df.drop(axis=1, labels=["release_date"])

save_path = os.path.join(save_dir, save_file)
df.to_csv(save_path, float_format="%.6f", compression="gzip", encoding="gb18030")
print(df)

if len(df) >= page_size:
    print("Warning! Length of downloaded data between {1} and {2} are larger than {0}, please try to split the period into more shorter ones".format(
        page_size, bgn_date, end_date
    ))
else:
    print(df)
