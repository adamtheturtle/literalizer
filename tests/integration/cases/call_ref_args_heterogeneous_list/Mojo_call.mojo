def process[*Ts: AnyType](*args: *Ts):
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
    process(my_ints^, 42)
    process(my_strings^, 7)
