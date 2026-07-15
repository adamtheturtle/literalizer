using System.Collections.Generic;
record Record0(string Name, Dictionary<string, object> Input, Dictionary<string, object> Expected);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0(
        "test_1",
        new Dictionary<string, object> {
            ["type"] = "create",
            ["pr_id"] = "pr_1",
            ["draft"] = true
        },
        new Dictionary<string, object> {
            ["pr_id"] = "pr_1",
            ["status"] = "draft"
        }
    ),
    new Record0(
        "test_2",
        new Dictionary<string, object> {
            ["type"] = "publish",
            ["pr_id"] = "pr_1"
        },
        new Dictionary<string, object> {
            ["error"] = "invalid_operation"
        }
    )
};
    }
}
