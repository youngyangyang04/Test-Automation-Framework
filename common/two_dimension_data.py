def print_table(two_dimension_list):
    """
    打印表格函数
    输入一个2维列表,格式参见:
    [
    ["123,"123,"123"],
    ["123,"123","123]
    ...
    ]
    空行表示方法:
    ["","",""]
    注意每行的元素数需要相等
    :param two_dimension_list:
    :return:
    """

    def sum_string_length(keys):
        length = 0
        for key in str(keys):
            if u'\u4e00' <= key <= u'\u9fff':
                length += 2
            elif u'\uFF01' <= key <= u'\uFF5E':
                length += 2
            else:
                length += 1
        return length

    four_space = "    "
    # 列表元素为每一列最长字符的长度, 列表长度等于每一行的元素数
    each_col_max_length_list = []
    # 一行的元素个数
    row_element_count = len(two_dimension_list[0])
    for col in range(row_element_count):
        max_length = 0
        for i in range(len(two_dimension_list)):
            element_length = sum_string_length(two_dimension_list[i][col])
            if max_length < element_length:
                max_length = element_length
        each_col_max_length_list.append(max_length)

    # 这个可以表示"|"的数量
    vertical_line_count = len(each_col_max_length_list)
    before_space_count = vertical_line_count * 4
    after_space_count = sum(each_col_max_length_list) + before_space_count
    line_count = before_space_count + after_space_count + vertical_line_count
    case_str = "+{0}+".format("-" * (line_count - 1))
    print(case_str)
    for row_num in range(len(two_dimension_list)):
        output_str = "|"
        for element in range(len(two_dimension_list[row_num])):
            later_space_count = each_col_max_length_list[element] - sum_string_length(
                two_dimension_list[row_num][element]) + 4
            # 减一表示"|"占用一个空格位置
            space1 = " " * (later_space_count)
            output_str += "{space0}{value}{space1}|".format(space0=four_space,
                                                            value=two_dimension_list[row_num][element],
                                                            space1=space1)
        # 判断是否空行
        if output_str.replace("|", "").replace(" ", ""):
            print(output_str)
        else:
            # 如果是空行
            output_str = "|"
            for i in range(len(two_dimension_list[row_num])):
                output_str += "-" * (each_col_max_length_list[i] + 8) + "+"
            output_str = output_str[:-1] + "|"
            print(output_str)
    # print(case_str)


test_list = [
    ['id', 'vehicle_no', 'color', 'address'],
    ["", "", "", ""],
    ['1116016058541708528', '京GW0001', '蓝色', '北京海淀'],
    ['1146003998720578844', '冀F12343', '黄色', '成都锦江'],
    ['1148015232542564762', '冀F12370', '绿色', '广州花都'],
    ["", "", "", ""]
]

# print_table(test_list)
