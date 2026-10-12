from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = List([
        {"nested": {"count": Value(1), "name": Value(String("value"))}},
        Dict[String, Dict[String, Value]](),
    ])
    _ = my_data
