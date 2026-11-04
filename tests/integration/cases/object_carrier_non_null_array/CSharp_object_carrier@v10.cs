
var my_data = new object[] {
    true,
    ""
};
object[] values = my_data;
if (values.Length != 2 || values[0] is not true || values[1] is not "") { throw new System.InvalidOperationException("changed collection values"); }
