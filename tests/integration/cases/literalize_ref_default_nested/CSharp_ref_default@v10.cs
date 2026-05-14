using System.Collections.Generic;
using System;
var item_var = new Dictionary<string, string> {
    ["_"] = "_"
};
var my_data = new Dictionary<string, object> {
    ["items"] = (item_var, new Dictionary<string, string> {["fallback"] = "value"})
};
