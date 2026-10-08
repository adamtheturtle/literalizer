using System.Collections.Generic;
using System;
var my_data = (
    new SortedDictionary<string, object> {["name"] = "Ada", ["active"] = true, ["count"] = 1, ["score"] = 1.5, ["missing"] = (object?)null, ["scores"] = (1, 2), ["child"] = new SortedDictionary<string, int> {["age"] = 3}},
    new SortedDictionary<string, object> {["name"] = "Bob", ["active"] = false, ["count"] = 2, ["score"] = 2.5, ["missing"] = (object?)null, ["scores"] = ValueTuple.Create(4), ["child"] = new SortedDictionary<string, int> {["age"] = 5}}
);
