from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
def main():
    var my_data = [
        Tuple("name", Value(String("Alice"))),
        Tuple("age", Value(30)),
        Tuple("active", Value(True)),
    ]
    _ = my_data
