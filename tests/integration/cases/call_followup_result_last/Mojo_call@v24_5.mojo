def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def make_widget(var first: Int, var second: Int) -> None:
    pass
def consume[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    var my_data = make_widget(42, 3)
    consume(3, literalizer_ref_value(my_data))
