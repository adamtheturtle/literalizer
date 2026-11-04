using System.Collections.Generic;
var my_data = new Dictionary<string, System.Object?> {
    ["flag"] = true,
    ["text"] = ""
};
System.Collections.Generic.Dictionary<string, object?> values = my_data;
if (values.Count != 2 || values["flag"] is not true || values["text"] is not "") { throw new System.InvalidOperationException("changed collection values"); }
