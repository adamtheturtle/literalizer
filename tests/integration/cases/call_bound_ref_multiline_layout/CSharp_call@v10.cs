using System;
class Check {
static object f(object value = null) => null;
    public static void Main() {
var ref_data = (
    (
        1,
        2
    ),
    (
        3,
        4
    )
);
f(ValueTuple.Create(
    ValueTuple.Create(
        ref_data
    )
));
    }
}
