from std.utils.variant import Variant
comptime JsonValue = Variant[String, Int, Float64, Bool, NoneType]
def main():
    var my_data = {
        "s": JsonValue(String("string")),
        "i": JsonValue(1),
        "f": JsonValue(Float64(1.5)),
        "b": JsonValue(True),
        "n": JsonValue(NoneType()),
        "d": JsonValue(String("2024-01-15")),
        "dt": JsonValue(String("2024-01-15T12:00:00")),
        "by": JsonValue(String("48656c6c6f")),
    }
    _ = my_data
