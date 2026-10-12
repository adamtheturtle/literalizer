from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = List([
        {"count": Value(1), "name": Value(String("value"))},
        Dict[String, Value](),
    ])
    _ = my_data
