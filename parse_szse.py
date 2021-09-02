import sys
import os
import re

report_date = sys.argv[1]
raw_dir = sys.argv[2]

for sector_type in ["a", "c"]:
    raw_file = "{}.public_info.SZ-{}.txt".format(report_date, sector_type)
    raw_path = os.path.join(raw_dir, raw_file)
    print(raw_path)
    with open(raw_path, "r", encoding="utf-8") as f:
        block_list = []
        detailed_info = False
        for raw_line in f.readlines():
            if len(raw_line.replace("\n", "").replace(" ", "")) == 0:
                continue

            if raw_line[0:4] == "详细信息":
                detailed_info = True
                continue

            if detailed_info:
                net_line = raw_line.replace("\n", "")
                if raw_line[0:20] == "-" * 20:
                    new_block = True
                    block_name = net_line.replace("：", "")
                    continue

                if re.search("(代码[0-9]{6})", net_line) is not None:
                    print(net_line)
