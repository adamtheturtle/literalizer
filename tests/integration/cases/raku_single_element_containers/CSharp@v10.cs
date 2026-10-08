using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["single_map"] = ValueTuple.Create(new Dictionary<string, object> {}),
    ["single_list"] = ValueTuple.Create(ValueTuple.Create(1)),
    ["single_deep"] = ValueTuple.Create(ValueTuple.Create(ValueTuple.Create(2)))
};
