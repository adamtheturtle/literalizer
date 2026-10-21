def consume_widget[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var shared = List([
        1,
        2,
    ])
    var my_data = shared.copy()
    consume_widget(my_data)
