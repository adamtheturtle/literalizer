fn process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_ints = [
        1,
        2,
        3,
    ]
    var my_strings = [
        "a",
        "b",
    ]
    var my_empty = List[String]()
    process(my_ints^, 42)
    process(my_strings^, 7)
    process(my_empty^, 99)
