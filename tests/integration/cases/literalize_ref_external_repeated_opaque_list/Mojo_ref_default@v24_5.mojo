def consume_widget[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var item = List[String]()
    var my_data = List([
        item.copy(),
        item.copy(),
    ])
    consume_widget(my_data)
