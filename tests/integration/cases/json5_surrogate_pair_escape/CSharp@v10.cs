using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["astral"] = "😀",
    ["mixed"] = "a😀b",
    ["count"] = 2,
    ["list"] = ("😀", 1),
    ["nested"] = new Dictionary<string, string> {["inner"] = "😀"}
};
