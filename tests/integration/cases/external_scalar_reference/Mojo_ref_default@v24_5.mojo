def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def consume_widget(var arg_value: Int):
    pass
def main():
    var shared = 1
    var my_data = shared
    consume_widget(literalizer_ref_value(my_data))
