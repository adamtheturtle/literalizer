from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = {
        1: [JsonValue(1), JsonValue(String("email")), JsonValue(String("a@gmail.com")), JsonValue(100)],
    }
    _ = my_data
