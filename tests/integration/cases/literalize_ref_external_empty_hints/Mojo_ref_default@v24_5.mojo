def consume_widget(arg_value: List[Int]):
    pass
def main():
    var item = List([
        1,
        2,
    ])
    var my_data = List([
        1,
        2,
    ])
    consume_widget(my_data)
    my_data = item.copy()
    consume_widget(my_data)
