using System.Collections.Generic;
using System;
var my_data = new SortedDictionary<string, object?> {
    ["test"] = (5, ("compile", "test")),
    ["package"] = (7, ("link", "test"))
};
    _ = my_data;
