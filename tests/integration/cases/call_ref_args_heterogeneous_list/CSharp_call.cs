using System;
class Check {
static object process(object data = null, object count = null) => null;
    public static void Main() {
var my_ints = (
    1,
    2,
    3
);
var my_strings = (
    "a",
    "b"
);
var my_empty = ValueTuple.Create();
process(my_ints, 42);
process(my_strings, 7);
process(my_empty, 99);
    }
}
