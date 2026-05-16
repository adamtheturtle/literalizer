from std.utils.variant import Variant
comptime Value = Variant[Int, String, Bool]
def main():
    var my_data = [
        Value(1),
        Value(String("email")),
        Value(True),
    ]
    _ = my_data
