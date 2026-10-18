using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["first"] = new Dictionary<string, object?> {["items"] = (1, new Dictionary<string, int> {["value"] = 2})},
    ["second"] = new Dictionary<string, object?> {["items"] = (1, new Dictionary<string, string> {["value"] = "s"})}
};
    _ = my_data;
