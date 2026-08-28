using System;
class Check {
static object process(object xs = null) => null;
    public static void Main() {
process((
    1,
    2
));
process(ValueTuple.Create(
    3
));
    }
}
