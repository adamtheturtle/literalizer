using System.Collections.Generic;
using System;
var my_var = new Dictionary<string, string> {
    ["_"] = "_"
};
var item_var = new Dictionary<string, string> {
    ["_"] = "_"
};
var my_data = new Dictionary<string, object> {
    ["key"] = my_var,
    ["items"] = (item_var, new Dictionary<string, string> {["fallback"] = "value"})
};
