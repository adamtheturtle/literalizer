from std.utils.variant import Variant
comptime Value = Variant[String, Bool]
def main():
    var my_data = [
        {"input": {"kind": Value(String("add")), "item_id": Value(String("item_1")), "urgent": Value(True)}, "expected": {"item_id": Value(String("item_1")), "state": Value(String("pending"))}},
        {"input": {"kind": Value(String("remove")), "item_id": Value(String("item_9"))}, "expected": {"error": Value(String("not_found"))}},
    ]
    _ = my_data
