using System.Collections.Generic;
using System;
class Check {
static object process(object data = null) => null;
    public static void Main() {
var my_var = 42;
var my_other = 7;
process((new Dictionary<string, string> {["ref"] = "my_var"}, 42, "static"));
process((new Dictionary<string, string> {["ref"] = "my_other"}, 7, "label"));
    }
}
