import sys
import os
from custom_class import *

pd.set_option("display.width", 0)

report_date = sys.argv[1]
raw_dir = sys.argv[2]

dfs_list = []

raw_file = "{}.public_info.SSE.txt".format(report_date)
raw_path = os.path.join(raw_dir, raw_file)
print(raw_path)
with open(raw_path, "r", encoding="utf-8") as f:
    # find all useful lines
    detailed_info = False
    net_lines_book = []
    for raw_line in f.readlines():
        net_line = raw_line.replace("\n", "").strip()

        if len(net_line.replace(" ", "")) == 0:
            continue

        if net_line[0:4] == "交易日期":
            detailed_info = True
            continue

        if detailed_info:
            net_lines_book.append(net_line)

    # parse useful line
    block_description = ""
    record_description = ""
    block_manager = CBlockManager(t_market="SSE")
    p_tradeBlock = None

    for net_line in net_lines_book:
        if net_line[0:20] == "-" * 20:
            continue

        if is_block_description_sse(t_net_line=net_line):  # "一、有价格涨跌幅限制的日收盘价格涨幅偏离值达到7%的前三只证券:"
            block_description = net_line[:-1]
            block_description = remove_big_chs_digit_sse(t_block_description=block_description)
            print(net_line)
            continue

        if net_line.find("式基金连续三个交易日内累计换手率达到20%") == 0:
            block_description += net_line
            print(net_line)
            continue

        if is_sub_title_sse(t_net_line=net_line):  # "1、A股"
            continue

        if is_table_column_names_sse(t_net_line=net_line):  # "证券代码      证券简称      偏离值%        成交量        成交金额(万元)"
            continue

        if is_table_item_sse(t_net_line=net_line):  # "(1)  603033      三维股份       9.43%         8090324           17335.26"
            continue

        if is_sec_title_line_sse(t_net_line=net_line):  # "证券代码: 603033                                                                    证券简称: 三维股份"
            p_tradeBlock = CTradeBlock(t_title_line=net_line, t_block_description=block_description, t_market=block_manager.get_market())
            block_manager.append(t_trade_block=p_tradeBlock)
            print(net_line)
            continue

        if is_sec_record_title_sse(t_net_line=net_line):
            record_description = net_line.split()[0]
            print(net_line)
            continue

        if (len(net_line) == 1) or (net_line == "上海证券交易所"):  # end of file
            continue

        p_tradeBlock.append(t_record_description=record_description, t_content_line=net_line)
        print(net_line)

    dfs_list.append(block_manager.to_DataFrame())

parsed_df = pd.concat(dfs_list, ignore_index=True, axis=0)
parsed_file = "{}.public_info.SSE.parsed.csv.gz".format(report_date)
parsed_path = os.path.join(raw_dir, parsed_file)
parsed_df.to_csv(parsed_path, index=False, float_format="%.2f", encoding="gb18030", compression="gzip")
