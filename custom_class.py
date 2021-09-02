from typing import List
import re
import pandas as pd


def is_title_line(t_net_line: str) -> bool:
    return re.search("\(代码[0-9]{6}\)", t_net_line) is not None


class CTradeRecordSZSE(object):
    def __init__(self, t_content_line: str):
        words = t_content_line.split()
        self.m_member_name: str = words[0]
        self.m_amt_b: float = float(words[1])
        self.m_amt_s: float = float(words[2])

    def to_dict(self):
        return {
            "会员": self.m_member_name,
            "买入金额": self.m_amt_b,
            "卖出金额": self.m_amt_s,
        }


class CTradeBlockSZSE(object):
    def __init__(self, t_title_line: str, t_block_description: str):
        bgn_loc, _ = re.search("\(代码[0-9]{6}\)", t_title_line).span()

        self.m_block_description: str = t_block_description
        self.m_wind_code: str = t_title_line[bgn_loc + 3:bgn_loc + 9] + ".SZ"
        self.m_chs_name: str = t_title_line[0:bgn_loc]

        self.m_max_b_records: List[CTradeRecordSZSE] = []
        self.m_max_s_records: List[CTradeRecordSZSE] = []

    def append(self, t_record_description: str, t_content_line: str):
        if t_record_description == "买入金额最大的前5名":
            self.m_max_b_records.append(CTradeRecordSZSE(t_content_line))
            return 0
        elif t_record_description == "卖出金额最大的前5名":
            self.m_max_s_records.append(CTradeRecordSZSE(t_content_line))
            return 0
        else:
            print("| {} | {} | Error! | {} | {} |".format(self.m_wind_code, self.m_chs_name, t_record_description, t_content_line))
            return -1

    def to_records_list(self):
        records = []
        for i, record in enumerate(self.m_max_b_records):
            d = record.to_dict()
            d.update({
                "异动类型": self.m_block_description,
                "标的代码": self.m_wind_code,
                "标的名称": self.m_chs_name,
                "排名类型": "买入前" + str(i + 1)
            })
            records.append(d)

        for i, record in enumerate(self.m_max_s_records):
            d = record.to_dict()
            d.update({
                "异动类型": self.m_block_description,
                "标的代码": self.m_wind_code,
                "标的名称": self.m_chs_name,
                "排名类型": "卖出前" + str(i + 1)
            })
            records.append(d)

        return records


class CBlockManager(object):
    def __init__(self):
        self.m_parsed_blocks: List[CTradeBlockSZSE] = []

    def append(self, t_trade_block: CTradeBlockSZSE):
        self.m_parsed_blocks.append(t_trade_block)
        return 0

    def to_DataFrame(self):
        all_records = []
        for block in self.m_parsed_blocks:
            all_records += block.to_records_list()
        res = pd.DataFrame(all_records)
        res = res[["异动类型", "标的代码", "标的名称", "会员", "排名类型", "买入金额", "卖出金额"]]
        return res
