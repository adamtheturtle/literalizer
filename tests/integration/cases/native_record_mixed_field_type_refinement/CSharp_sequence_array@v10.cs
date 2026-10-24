using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["first"] = new Dictionary<string, object?> {["items"] = new object?[] {1, new Dictionary<string, int> {["value"] = 2}}},
    ["second"] = new Dictionary<string, object?> {["items"] = new object?[] {1, new Dictionary<string, string> {["value"] = "s"}}}
};
    _ = my_data;
