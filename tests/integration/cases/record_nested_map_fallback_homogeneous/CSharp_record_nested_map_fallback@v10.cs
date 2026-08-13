using System.Collections.Generic;
record Record1(string Kind, string PrId);
record Record0(string Name, Record1 Input, Dictionary<string, string> Expected);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0("test_1", new Record1("create", "pr_1"), new Dictionary<string, string> {["pr_id"] = "pr_1", ["status"] = "draft"}),
    new Record0("test_2", new Record1("publish", "pr_1"), new Dictionary<string, string> {["error"] = "invalid_operation"})
};
    }
}
