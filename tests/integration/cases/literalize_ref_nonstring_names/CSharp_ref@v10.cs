using System.Collections.Generic;
using System;
var Actual = new Dictionary<string, object> {
    ["_"] = "_"
};
var my_data = (
    new Dictionary<string, object> {["$ref"] = 1},
    new Dictionary<string, object> {["$ref"] = (object?)null},
    Actual
);
