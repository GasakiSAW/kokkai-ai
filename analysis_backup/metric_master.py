METRIC_MASTER = {

    "完全失業率": {
        "stats_data_id": "0000010206",
        "title": "完全失業率",
        "rule": "lower_is_better"
    },

    "失業率": {
        "stats_data_id": "0000010206",
        "title": "完全失業率",
        "rule": "lower_is_better"
    },

    "消費者物価指数": {
        "stats_data_id": "0002050001",
        "title": "消費者物価指数",
        "rule": "depends"
    },

    "実質賃金": {
        "stats_data_id": "0003030252",
        "title": "実質賃金指数",
        "rule": "higher_is_better"
    },

    "出生数": {
        "stats_data_id": "0003411595",
        "title": "年次別にみた出生数・出生率・出生性比・合計特殊出生率",
        "rule": "higher_is_better"
    },

    "合計特殊出生率": {
        "stats_data_id": "0003411595",
        "title": "年次別にみた出生数・出生率・出生性比・合計特殊出生率",
        "rule": "higher_is_better"
    },

    "GDP": {
        "stats_data_id": "",
        "title": "国内総生産",
        "rule": "higher_is_better"
    },

    "国内総生産": {
        "stats_data_id": "",
        "title": "国内総生産",
        "rule": "higher_is_better"
    }
}


def get_master_metric(metric):

    return METRIC_MASTER.get(metric)
