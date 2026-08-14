using System.Collections.Generic;
record Record0(string Name, Dictionary<string, object> Payload);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0("one", new Dictionary<string, object> {["scalar"] = 1, ["items"] = new int[] {2, 3}}),
    new Record0("two", new Dictionary<string, object> {["other"] = 2})
};
    }
}
