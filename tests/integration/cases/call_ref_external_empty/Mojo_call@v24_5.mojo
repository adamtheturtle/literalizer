def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def consume[*Ts: Movable](var *args: *Ts):
    pass
def main():
    var item = List([
        1,
        2,
    ])
    consume(item^)
