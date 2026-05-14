from std.utils.variant import Variant
comptime JsonValue = Variant[String, Int, Bool, Float64]
def main():
    var my_data = {
        "name": JsonValue(String("Alice")),
        "age": JsonValue(30),
        "active": JsonValue(True),
        "score": JsonValue(Float64(4.5)),
    }
    _ = my_data
