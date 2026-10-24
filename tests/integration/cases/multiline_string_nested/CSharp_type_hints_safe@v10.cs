using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["outer"] = ValueTuple.Create(ValueTuple.Create("nested first line\n  indented\n\nnested last line\n"))
};
    _ = my_data;
