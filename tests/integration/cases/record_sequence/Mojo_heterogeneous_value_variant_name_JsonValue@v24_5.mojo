from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = [
        {"id": JsonValue(1), "label": JsonValue(String("first"))},
        {"id": JsonValue(2), "label": JsonValue(String("second"))},
        {"id": JsonValue(3), "label": JsonValue(String("third"))},
    ]
    _ = my_data
