from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = [
        {"id": Value(1), "label": Value(String("first"))},
        {"id": Value(2), "label": Value(String("second"))},
        {"id": Value(3), "label": Value(String("third"))},
    ]
    _ = my_data
