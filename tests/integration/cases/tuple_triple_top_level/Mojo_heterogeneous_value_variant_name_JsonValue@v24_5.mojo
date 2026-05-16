from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String, Bool]
def main():
    var my_data = [
        JsonValue(1),
        JsonValue(String("email")),
        JsonValue(True),
    ]
    _ = my_data
