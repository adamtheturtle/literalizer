def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def process(var data: List[Int]):
    pass
def main():
    var unknown_value = List([
        1,
    ])
    process(literalizer_ref_value(unknown_value))
