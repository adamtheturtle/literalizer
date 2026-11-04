using System.Collections.Generic;
var my_data = new HashSet<object?> {
    (object?)null,
    true
};
System.Collections.Generic.HashSet<object?> values = my_data;
if (values.Count != 2 || !values.Contains(true) || !values.Contains(null)) { throw new System.InvalidOperationException("changed collection values"); }
