import sys
import os
from custom_class import *

pd.set_option("display.width", 0)

report_date = sys.argv[1]
raw_dir = sys.argv[2]

dfs_list = []
for sector_type in ["a", "c"]:
    raw_file = "{}.public_info.SZ-{}.txt".format(report_date, sector_type)
    raw_path = os.path.join(raw_dir, raw_file)
    with open(raw_path, "r", encoding="utf-8") as f:
        # find all useful lines
        detailed_info = False
        net_lines_book = []
        for raw_line in f.readlines():
            net_line = raw_line.replace("\n", "")

            if len(net_line.replace(" ", "")) == 0:
                continue

            if net_line[0:4] == "详细信息":
                detailed_info = True
                continue

            if detailed_info:
                net_lines_book.append(net_line)

        # parse useful line
        next_line_is_block_description = False
        block_description = ""
        record_description = ""
        block_manager = CBlockManager(t_market="SZSE")
        p_tradeBlock = None
        for net_line in net_lines_book:
            if net_line[0:20] == "-" * 20:
                next_line_is_block_description = True
                continue

            if next_line_is_block_description:
                block_description = net_line[:-1]
                next_line_is_block_description = False
                print(net_line)
                continue

            if is_title_line_szse(t_net_line=net_line):  # "*ST金正(代码002470)              成交量:12329万份/万股  成交金额:34841万元"
                p_tradeBlock = CTradeBlock(t_title_line=net_line, t_block_description=block_description, t_market=block_manager.get_market())
                block_manager.append(t_trade_block=p_tradeBlock)
                print(net_line)
                continue

            if net_line.find("异常期间") == 0:  # "异常期间:2021/08/25至2021/08/27   累计涨幅偏离值:15.97%"
                continue

            if net_line in ["买入金额最大的前5名", "卖出金额最大的前5名"]:  # "买入金额最大的前5名" "卖出金额最大的前5名"
                record_description = net_line
                continue

            if net_line.find("营业部或交易单元名称") == 0:  # "营业部或交易单元名称                                  买入金额(元)  卖出金额(元)"
                continue

            if net_line.find("日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20%的证券") == 0:
                block_description += "，日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20%的证券"
                print(net_line)
                continue

            p_tradeBlock.append(t_record_description=record_description, t_content_line=net_line)
            print(net_line)

        dfs_list.append(block_manager.to_DataFrame())

parsed_df = pd.concat(dfs_list, ignore_index=True, axis=0)
parsed_file = "{}.public_info.SZSE.parsed.csv.gz".format(report_date)
parsed_path = os.path.join(raw_dir, parsed_file)
parsed_df.to_csv(parsed_path, index=False, float_format="%.2f", encoding="gb18030", compression="gzip")
