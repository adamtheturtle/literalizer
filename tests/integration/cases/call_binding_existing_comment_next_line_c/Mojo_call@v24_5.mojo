def make_widget[*Ts: AnyType](*args: *Ts) -> None:
    pass
def main():
    var my_data = make_widget(42)
    my_data = make_widget(my_data)
    // note
    make_widget(my_data)
