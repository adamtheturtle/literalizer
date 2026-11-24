def make_widget(var count: Int) -> None:
    pass
def consume_widget[*Ts: Movable](var *args: *Ts):
    pass
def main():
    var my_data = make_widget(0)
    consume_widget(my_data)
    my_data = make_widget(1)
    consume_widget(my_data)
