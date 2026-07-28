using System.Collections.Generic;
using System;
class Check {
static object process(object data = null) => null;
    public static void Main() {
var my_list = new Dictionary<string, string> {
    ["unused"] = "value"
};
process(((new Dictionary<string, object> {["inner"] = my_list})));
    }
}
