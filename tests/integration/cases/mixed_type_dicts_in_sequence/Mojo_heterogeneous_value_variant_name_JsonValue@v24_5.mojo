from std.utils.variant import Variant
comptime JsonValue = Variant[String, Bool]
def main():
    var my_data = [
        {"type": JsonValue(String("create")), "pr_id": JsonValue(String("pr_1")), "draft": JsonValue(True)},
        {"type": JsonValue(String("create")), "pr_id": JsonValue(String("pr_2"))},
    ]
    _ = my_data
