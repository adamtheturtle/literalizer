using System.Collections.Generic;
using System;
class Check {
static object process(object value = null) => null;
static object emit(object _call = null, object _zip = null) => null;
    public static void Main() {
emit(process("hello"), new Dictionary<string, int> {["a"] = 1, ["b"] = 2});
emit(process(42), new Dictionary<string, int> {["c"] = 3, ["d"] = 4});
    }
}
