def make_widget[*Ts: AnyType](*args: *Ts) -> None:
    pass
def main():
    var my_data = make_widget(42)
    make_widget(my_data)
    my_data = make_widget(my_data) // note
    // extra
    make_widget(my_data)
