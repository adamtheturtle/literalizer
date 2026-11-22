using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {};
System.Collections.Generic.Dictionary<string, object?> values = my_data;
if (values.Count != 0) { throw new System.InvalidOperationException("changed collection values"); }
