from std.utils.variant import Variant
comptime Value = Variant[String, Bool]
def main():
    var my_data = [
        {"type": Value(String("create")), "pr_id": Value(String("pr_1")), "draft": Value(True)},
        {"type": Value(String("create")), "pr_id": Value(String("pr_2"))},
    ]
    _ = my_data
