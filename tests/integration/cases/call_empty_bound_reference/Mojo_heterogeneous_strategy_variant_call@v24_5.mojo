def make_widget[*Ts: AnyType](var *args: *Ts) -> None:
    pass
def main():
    var items = List[String]()
    make_widget(items.copy())
