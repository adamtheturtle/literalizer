using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object?> {["nested"] = new Dictionary<string, object?> {["times"] = ValueTuple.Create("1900-01-01T00:00:00+00:00")}},
    new Dictionary<string, object?> {}
);
    _ = my_data;
