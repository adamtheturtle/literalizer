import tables
var my_data = {
    "omap_value": {"first": 1}.toOrderedTable,
    "sibling_lists": {"numbers": @[1, 2], "strings": @["x", "y"]}.toTable,
    "ref_marker_present": @["$keep", "z"]
}.toTable
