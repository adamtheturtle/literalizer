from std.utils.variant import Variant
comptime Value = Variant[String, Int]
def main():
    var my_data = [
        Value(String("hello")),
        Value(42),
    ]
    _ = my_data
