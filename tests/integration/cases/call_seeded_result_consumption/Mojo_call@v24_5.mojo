def make_widget[*Ts: AnyType](*args: *Ts) -> None:
    pass
def consume_widget[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_data = make_widget(0)
    consume_widget(my_data)
    my_data = make_widget(1)
    consume_widget(my_data)
