def literalizer_ref_value(value: None) -> None:
    return None

def literalizer_ref_value[T: Copyable](value: T) -> T:
    return value.copy()
def process(var data: List[List[Dict[String, Dict[String, String]]]]):
    pass
def main():
    var my_list = {
        "unused": "value",
    }
    process(List([List([{"inner": my_list^}])]))
