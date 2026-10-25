def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def consume_widget[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    var item = None
    var my_data = None
    consume_widget(literalizer_ref_value(my_data))
    my_data = item
    consume_widget(literalizer_ref_value(my_data))
