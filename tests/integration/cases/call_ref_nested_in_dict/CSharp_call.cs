using System.Collections.Generic;
using System;
class Check {
static object process(object data = null) => null;
    public static void Main() {
var my_var = 42;
process(new Dictionary<string, object> {["key"] = new Dictionary<string, string> {["ref"] = "my_var"}, ["count"] = 42});
    }
}
