from std.utils.variant import Variant
comptime JsonValue = Variant[Int, String]
def main():
    var my_data = {
        "omap_value": [Tuple("first", 1)],
        "sibling_lists": {"numbers": [JsonValue(1), JsonValue(2)], "strings": [JsonValue(String("x")), JsonValue(String("y"))]},
        "ref_marker_present": ["$keep", "z"],
    }
    _ = my_data
