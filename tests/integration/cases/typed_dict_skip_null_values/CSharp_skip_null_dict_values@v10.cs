using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["divergent"] = (new Dictionary<string, object> {["b"] = 1}, new Dictionary<string, object> {["a"] = "hello"}),
    ["matching"] = (new Dictionary<string, int> {["n"] = 1}, new Dictionary<string, int> {["n"] = 2})
};
