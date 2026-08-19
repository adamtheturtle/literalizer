from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = List([
        List([JsonValue(1), JsonValue(String("a"))]),
        List([JsonValue(2), JsonValue(String("b"))]),
    ])
    _ = my_data
