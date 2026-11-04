
var my_data = new object[] {
    new object?[] {(object?)null},
    true
};
object[] values = my_data;
if (values.Length != 2 || values[0] is not object?[] inner || inner.Length != 1 || inner[0] is not null || values[1] is not true) { throw new System.InvalidOperationException("changed collection values"); }
