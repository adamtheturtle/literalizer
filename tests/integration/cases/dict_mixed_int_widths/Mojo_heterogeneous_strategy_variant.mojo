from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = {
        "a": Value(1),
        "b": Value(3000000000),
        "c": Value(String("x")),
    }
    _ = my_data
