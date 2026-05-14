using System.Collections.Generic;
using System;
class Check {
static object process(object value = null) => null;
    public static void Main() {
// Test cases
process(new Dictionary<string, string> {["type"] = "create", ["pr_id"] = "pr_1"});  // first case
process(new Dictionary<string, string> {["type"] = "update", ["pr_id"] = "pr_2"});  // second case
// third case
process(new Dictionary<string, string> {["type"] = "delete", ["pr_id"] = "pr_3"});
    }
}
