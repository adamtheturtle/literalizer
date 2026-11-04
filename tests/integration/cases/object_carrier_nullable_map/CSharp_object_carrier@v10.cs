using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["flag"] = true,
    ["nothing"] = (object?)null
};
System.Collections.Generic.Dictionary<string, object?> values = my_data;
if (values.Count != 2 || values["flag"] is not true || values["nothing"] is not null) { throw new System.InvalidOperationException("changed collection values"); }
