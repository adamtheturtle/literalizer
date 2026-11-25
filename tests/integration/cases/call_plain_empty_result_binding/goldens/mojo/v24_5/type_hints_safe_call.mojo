def make_widget[*Ts: Movable](var *args: *Ts) -> None:
    pass
def main():
    var my_data = make_widget(List[String]())
    _ = my_data
