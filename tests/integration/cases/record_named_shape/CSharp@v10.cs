using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object> {["id"] = 100, ["label"] = "first entry", ["enabled"] = false, ["related_ids"] = (102, 103)},
    new Dictionary<string, object> {["id"] = 101, ["label"] = "second entry", ["enabled"] = true, ["related_ids"] = (100)}
);
