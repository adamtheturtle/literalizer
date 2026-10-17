def consume_widget[*Ts: AnyType](*args: *Ts):
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
    my_data = item^
    consume_widget(my_data)
