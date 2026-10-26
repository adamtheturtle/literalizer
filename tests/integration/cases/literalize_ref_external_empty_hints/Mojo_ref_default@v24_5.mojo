def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def consume_widget(var arg_value: List[Int]):
    pass
def main():
    var item = List([
        1,
        2,
    ])
    var my_data = List([
        1,
        2,
    ])
    consume_widget(literalizer_ref_value(my_data))
    my_data = literalizer_ref_value(item)
    consume_widget(literalizer_ref_value(my_data))
