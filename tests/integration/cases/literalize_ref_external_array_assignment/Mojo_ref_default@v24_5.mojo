def consume_widget(arg_value: List[Int]):
    pass
def main():
    var shared = List([
        1,
        2,
    ])
    var my_data = List([
        0,
    ])
    consume_widget(my_data)
    my_data = shared.copy()
    consume_widget(my_data)
