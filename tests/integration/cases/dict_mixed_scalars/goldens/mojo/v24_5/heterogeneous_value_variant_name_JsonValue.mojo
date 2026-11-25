from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = {
        "a": JsonValue(1),
        "b": JsonValue(String("x")),
    }
    _ = my_data
