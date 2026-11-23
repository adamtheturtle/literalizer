static void CheckValue(object?[] values) {
    if (values.Length != 2 || values[0] is not true || values[1] is not "") {
        throw new System.InvalidOperationException("changed collection values");
    }
}
var my_data = new dynamic[] {
    true,
    ""
};
CheckValue(my_data);
