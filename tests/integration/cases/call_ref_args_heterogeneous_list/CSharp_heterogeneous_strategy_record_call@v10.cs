using System;
using System.Collections.Generic;
class Check {
static object process(object data = null, object count = null) => null;
    public static void Main() {
var my_ints = new int[] {
    1,
    2,
    3
};
var my_strings = new string[] {
    "a",
    "b"
};
var my_empty = Array.Empty<object>();
process(my_ints, 42);
process(my_strings, 7);
process(my_empty, 99);
    }
}
