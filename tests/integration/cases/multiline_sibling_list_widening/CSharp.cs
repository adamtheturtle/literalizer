using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["omap_value"] = new Dictionary<string, object> {["first"] = 1},
    ["sibling_lists"] = new Dictionary<string, object> {["numbers"] = (1, 2), ["strings"] = ("x", "y")},
    ["ref_marker_present"] = ("$keep", "z")
};
