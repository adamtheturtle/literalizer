using System;
class Check {
static object f(object value = null) => null;
    public static void Main() {
var x = (
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
        x
    )
));
    }
}
