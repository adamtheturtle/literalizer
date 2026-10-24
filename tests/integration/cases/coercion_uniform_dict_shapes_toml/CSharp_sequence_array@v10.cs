using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["_"] = new Dictionary<string, string>[] {new Dictionary<string, string> {["type"] = "create", ["name"] = "a"}, new Dictionary<string, string> {["type"] = "update", ["name"] = "b"}}
};
    _ = my_data;
