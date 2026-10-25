def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var unknown_value = List[String]()
    process(literalizer_ref_value(unknown_value))
