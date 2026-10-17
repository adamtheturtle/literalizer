def consume_widget[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var ref_data = List([
        1,
        2,
    ])
    var my_data = List([
        0,
    ])
    consume_widget(my_data)
    my_data = ref_data.copy()
    consume_widget(my_data)
