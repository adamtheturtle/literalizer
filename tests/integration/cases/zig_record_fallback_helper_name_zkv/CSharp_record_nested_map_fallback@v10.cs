using System.Collections.Generic;
record Record0(string Name, Dictionary<string, object> Payload);
class Check {
    public static void Main() {
var ZKV = new[] {
    new Record0("ZVal ZKV literalizer record value", new Dictionary<string, object> {["scalar"] = 1, ["items"] = new HashSet<int> {2, 3}}),
    new Record0("two", new Dictionary<string, object> {["other"] = 2})
};
    }
}
