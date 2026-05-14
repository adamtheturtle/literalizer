from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String, NoneType]
def main():
    var my_data = {
        "outer": {"a": JsonValue(1), "b": JsonValue(String("x")), "c": JsonValue(NoneType())},
    }
    _ = my_data
