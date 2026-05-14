from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool, Float64]
def main():
    var my_data = {
        "name": Value(String("Alice")),
        "age": Value(30),
        "active": Value(True),
        "score": Value(Float64(4.5)),
    }
    _ = my_data
