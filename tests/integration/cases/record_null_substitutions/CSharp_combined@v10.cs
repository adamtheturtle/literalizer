using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object> {["missing"] = (object?)null, ["present"] = 1},
    new Dictionary<string, object> {["missing"] = 2, ["present"] = 3}
);
my_data = (
    new Dictionary<string, object> {["missing"] = (object?)null, ["present"] = 1},
    new Dictionary<string, object> {["missing"] = 2, ["present"] = 3}
);
