def make_widget[*Ts: Movable](var *args: *Ts) -> None:
    pass
def main():
    var items = List[String]()
    make_widget(items.copy())
