using System.Collections.Generic;
using System;
class Check {
static object? consume(object? value = null) => null;
    public static void Main() {
var item = 42;
consume(new Dictionary<string, int> {["field"] = item});
    }
}
