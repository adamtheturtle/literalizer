def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def make_widget(var value: Int) -> None:
    pass
def consume[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    var my_data = make_widget(42)
    consume(literalizer_ref_value(my_data))
