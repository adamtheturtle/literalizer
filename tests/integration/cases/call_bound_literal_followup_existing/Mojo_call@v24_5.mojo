def make_widget(var value: Int) -> None:
    pass
def consume[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    var my_data = make_widget(42)
    consume(my_data)
    my_data = make_widget(42)
    consume(my_data)
