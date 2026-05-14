from std.utils.variant import Variant
comptime JsonValue = Variant[String, Int]
def main():
    var my_data = [
        JsonValue(String("hello")),
        JsonValue(42),
    ]
    _ = my_data
