using System.Collections.Generic;
using System;
var Actual = 42;
var my_data = (
    new Dictionary<string, object> {["$ref"] = 1},
    new Dictionary<string, object> {["$ref"] = (object?)null},
    Actual
);
