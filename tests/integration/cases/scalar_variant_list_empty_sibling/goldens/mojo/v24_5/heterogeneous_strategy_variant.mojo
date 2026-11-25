from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = List([
        List([Value(1), Value(String("value"))]),
        List[Value](),
    ])
    _ = my_data
