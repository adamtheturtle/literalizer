from std.utils.variant import Variant
comptime Value = Variant[String]
def main():
    var my_data = {
        "vals": [Value(String("09:30:00")), Value(String("hello"))],
    }
    _ = my_data
