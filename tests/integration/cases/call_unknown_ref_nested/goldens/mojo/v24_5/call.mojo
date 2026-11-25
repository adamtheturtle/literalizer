def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def process(var known_value: Bool, var nested_missing: Bool):
    pass
def main():
    var known_value = True
    var unknown_value = True
    process(known_value, literalizer_ref_value(unknown_value))
