using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["test"] = (5, ValueTuple.Create("compile")),
    ["package"] = (7, ("link", "test"))
};
