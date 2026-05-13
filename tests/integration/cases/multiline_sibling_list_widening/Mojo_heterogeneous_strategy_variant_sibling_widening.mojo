from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def main():
    var my_data = {
        "omap_value": [Tuple("first", 1)],
        "sibling_lists": {"numbers": [Value(1), Value(2)], "strings": [Value(String("x")), Value(String("y"))]},
        "ref_marker_present": ["$keep", "z"],
    }
    _ = my_data
