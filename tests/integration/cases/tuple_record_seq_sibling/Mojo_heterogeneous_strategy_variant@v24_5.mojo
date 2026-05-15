from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = {
        "scores": [Value(10), Value(20), Value(30)],
        "args": [Value(1), Value(String("email")), Value(String("a@gmail.com")), Value(100)],
    }
    _ = my_data
