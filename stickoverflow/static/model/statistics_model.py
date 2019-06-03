from statistics import median, mean
from collections import Counter
from numpy import bincount
from pandas import DataFrame, read_csv
from json import dumps

# return list
def result(file_path, option = 0, x_label_col = 1, y_label_col = 2):
    df = read_csv(file_path)
    slt_list = list(set(df[col_name]))
    lst = list()

    for slt in slt_list:
        data_list = list(df.loc[df[col_name] == slt][col_name2])
        lst.append([slt, get_data_by_option(data_list, option)])
    return lst

# return numeric
def get_data_by_option(data_list, option):
    rst = 0

    if option == 0:
        rst = round(mean(data_list),3)
    elif option == 1:
        rst = median(data_list)
    elif option == 2:
        rst = max(data_list)
    elif option == 3:
        rst = min(data_list)
    elif option == 4:
        rst = bincount(data_list).argmax()

    return rst

# return str
def get_graph_data(data_table, chart_type = 'LineChart', options = {'title' : 'Example'}, container_id = 'chart_div'):
    data = dict()
    data['chartType'] = chart_type
    data['dataTable'] = data_table
    data['options'] = options
    data['containerId'] = container_id

    return dumps(data)
