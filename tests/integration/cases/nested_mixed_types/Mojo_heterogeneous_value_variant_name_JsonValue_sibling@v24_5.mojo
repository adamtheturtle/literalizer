from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = List([
        List([JsonValue(1), JsonValue(2)]),
        List([JsonValue(String("a")), JsonValue(String("b"))]),
    ])
    _ = my_data
