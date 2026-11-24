from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = List([
        JsonValue(1),
        JsonValue(String("email")),
    ])
    _ = my_data
