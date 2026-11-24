using System.Collections.Generic;
static void CheckValue(System.Collections.Generic.Dictionary<string, object?> values) {
    if (values.Count != 0) {
        throw new System.InvalidOperationException("changed collection values");
    }
}
var my_data = new Dictionary<string, object?> {};
CheckValue(my_data);
