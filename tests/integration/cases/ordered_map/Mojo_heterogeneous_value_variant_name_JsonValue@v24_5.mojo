from std.utils.variant import Variant
comptime JsonValue = Variant[String, Int, Bool]
def main():
    var my_data = [
        Tuple("name", JsonValue(String("Alice"))),
        Tuple("age", JsonValue(30)),
        Tuple("active", JsonValue(True)),
    ]
    _ = my_data
