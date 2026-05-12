from std.utils.variant import Variant
comptime Value = Variant[List[Int], List[String]]
def process(data: Value, count: Int):
    pass
def main():
    var my_ints = [
        1,
        2,
        3,
    ]
    var my_strings: List[String] = [
        "a",
        "b",
    ]
    process(my_ints^, 42)
    process(my_strings^, 7)
