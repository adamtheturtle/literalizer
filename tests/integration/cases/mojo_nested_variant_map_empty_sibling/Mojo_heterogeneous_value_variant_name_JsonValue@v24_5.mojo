from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = List([
        {"nested": {"count": JsonValue(1), "name": JsonValue(String("value"))}},
        Dict[String, Dict[String, JsonValue]](),
    ])
    _ = my_data
