using System.Collections.Generic;
class Check {
static object process(object value = null) => null;
    public static void Main() {
process(new Dictionary<string, object> {["value"] = 1});
process(new Dictionary<string, object> {["value"] = "hello"});
    }
}
