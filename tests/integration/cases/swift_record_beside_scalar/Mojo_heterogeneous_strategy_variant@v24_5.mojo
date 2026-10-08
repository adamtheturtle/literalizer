from std.utils.variant import Variant
comptime Value = Variant[Dict[String, Int], Int]
def main():
    var my_data = List([
        {"a": 1},
        5,
    ])
    _ = my_data
