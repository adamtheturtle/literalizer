using System.Collections.Generic;
record Record0(Dictionary<string, object> Input);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0(new Dictionary<string, object> {["a"] = 1}),
    new Record0(new Dictionary<string, object> {["b"] = (object?)null})
};
    }
}
