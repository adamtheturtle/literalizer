
var my_data = new object?[] {};
object?[] values = my_data;
if (values.Length != 0) { throw new System.InvalidOperationException("changed collection values"); }
