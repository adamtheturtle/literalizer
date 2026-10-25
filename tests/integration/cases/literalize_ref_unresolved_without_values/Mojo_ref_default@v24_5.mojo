def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def consume_widget(arg_value: List[Int]):
    pass
def main():
    var a = 0
    var my_data = List([
        literalizer_ref_value(a),
        1,
    ])
    consume_widget(literalizer_ref_value(my_data))
