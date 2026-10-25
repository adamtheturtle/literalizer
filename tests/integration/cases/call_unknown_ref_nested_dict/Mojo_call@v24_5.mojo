def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def process[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    var my_list = {
        "unused": "value",
    }
    process(List([List([{"inner": my_list^}])]))
