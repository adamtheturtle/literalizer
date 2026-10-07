using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = ValueTuple.Create(ValueTuple.Create(new Dictionary<string, int> {["b"] = 1}))
};
my_data = new Dictionary<string, object> {
    ["a"] = ValueTuple.Create(ValueTuple.Create(new Dictionary<string, int> {["b"] = 1}))
};
