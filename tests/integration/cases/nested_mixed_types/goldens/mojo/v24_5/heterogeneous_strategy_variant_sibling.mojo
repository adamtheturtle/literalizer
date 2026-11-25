from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = List([
        List([Value(1), Value(2)]),
        List([Value(String("a")), Value(String("b"))]),
    ])
    _ = my_data
