using System.Collections.Generic;
var my_data = new HashSet<object?>();
System.Collections.Generic.HashSet<object?> values = my_data;
if (values.Count != 0) { throw new System.InvalidOperationException("changed collection values"); }
