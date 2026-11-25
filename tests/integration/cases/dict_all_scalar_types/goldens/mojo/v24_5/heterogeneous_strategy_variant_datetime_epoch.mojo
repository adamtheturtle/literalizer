from std.utils.variant import Variant
comptime Value = Variant[String, Int, Float64, Bool, NoneType]
def main():
    var my_data = {
        "s": Value(String("string")),
        "i": Value(1),
        "f": Value(Float64(1.5)),
        "b": Value(True),
        "n": Value(NoneType()),
        "d": Value(String("2024-01-15")),
        "dt": Value(1705320000),
        "by": Value(String("48656c6c6f")),
    }
    _ = my_data
