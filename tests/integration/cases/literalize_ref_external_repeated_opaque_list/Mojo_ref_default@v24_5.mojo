def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def consume_widget[*Ts: Movable](var *args: *Ts):
    pass
def main():
    var item = List[String]()
    var my_data = List([
        literalizer_ref_value(item),
        literalizer_ref_value(item),
    ])
    consume_widget(literalizer_ref_value(my_data))
