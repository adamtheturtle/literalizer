using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["project"] = "alpha",
    ["lead_item"] = new Dictionary<string, object> {["id"] = 100, ["label"] = "first item", ["enabled"] = false, ["related_ids"] = (102, 103)}
};
