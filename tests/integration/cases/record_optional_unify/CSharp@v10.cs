using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["items"] = (new Dictionary<string, int> {["id"] = 1}, new Dictionary<string, int> {["id"] = 2, ["count"] = 10}, new Dictionary<string, int> {["id"] = 3, ["count"] = 20})
};
