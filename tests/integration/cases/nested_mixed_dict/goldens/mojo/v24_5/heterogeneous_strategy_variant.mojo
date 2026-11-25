from std.utils.variant import Variant
comptime Value = Variant[Int, String, NoneType]
def main():
    var my_data = {
        "outer": {"a": Value(1), "b": Value(String("x")), "c": Value(NoneType())},
    }
    _ = my_data
