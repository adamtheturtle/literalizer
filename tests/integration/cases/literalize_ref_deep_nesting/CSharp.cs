using System.Collections.Generic;
var my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, object> {["b"] = new Dictionary<string, object> {["c"] = new Dictionary<string, string> {["$ref"] = "deep"}}}
};
