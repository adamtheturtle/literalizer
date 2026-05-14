using System.Collections.Generic;
var Deep = new Dictionary<string, string> {
    ["_"] = "_"
};
var my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, object> {["b"] = new Dictionary<string, object> {["c"] = Deep}}
};
