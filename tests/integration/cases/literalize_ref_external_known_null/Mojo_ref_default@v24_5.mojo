def consume_widget[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var item = None
    var my_data = None
    consume_widget(my_data)
    my_data = item
    consume_widget(my_data)
