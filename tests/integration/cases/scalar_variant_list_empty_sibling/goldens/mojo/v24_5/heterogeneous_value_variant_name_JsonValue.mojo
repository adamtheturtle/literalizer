from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = List([
        List([JsonValue(1), JsonValue(String("value"))]),
        List[JsonValue](),
    ])
    _ = my_data
