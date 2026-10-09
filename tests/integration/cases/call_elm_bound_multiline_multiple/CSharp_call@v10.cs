using System;
class Check {
static object f(object value = null) => null;
    public static void Main() {
var ref_data = (
    1,
    2
);
f(ValueTuple.Create(
    ref_data
));
f(ValueTuple.Create(
    ref_data
));
    }
}
