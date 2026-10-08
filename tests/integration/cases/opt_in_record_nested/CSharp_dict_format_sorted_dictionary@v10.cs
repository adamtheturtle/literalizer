using System.Collections.Generic;
using System;
var my_data = new SortedDictionary<string, object> {
    ["owner"] = new SortedDictionary<string, object> {["name"] = "Ada", ["active"] = false},
    ["members"] = (new SortedDictionary<string, object> {["name"] = "Ada", ["score"] = 1.5}, new SortedDictionary<string, object> {["name"] = "Bob", ["score"] = 2.5})
};
