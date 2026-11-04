
var my_data = new object?[] {
    true,
    (object?)null
};
object?[] values = my_data;
if (values.Length != 2 || values[0] is not true || values[1] is not null) { throw new System.InvalidOperationException("changed collection values"); }
