from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = [
        [JsonValue(1), JsonValue(2)],
        [JsonValue(String("a")), JsonValue(String("b"))],
    ]
    _ = my_data
