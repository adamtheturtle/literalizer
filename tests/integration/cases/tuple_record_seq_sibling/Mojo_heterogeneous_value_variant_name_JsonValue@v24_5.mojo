from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = {
        "scores": [JsonValue(10), JsonValue(20), JsonValue(30)],
        "args": [JsonValue(1), JsonValue(String("email")), JsonValue(String("a@gmail.com")), JsonValue(100)],
    }
    _ = my_data
