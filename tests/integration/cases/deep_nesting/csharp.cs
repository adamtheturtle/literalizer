using System.Collections.Generic;
var x = new Dictionary<string, object> {
    ["level1"] = new Dictionary<string, object> {["level2"] = new Dictionary<string, object> {["level3"] = new Dictionary<string, object> {["level4"] = new Dictionary<string, object> {["value"] = "deep", ["items"] = new string[] {"a", "b"}}}, ["sibling"] = 42}, ["tags"] = new object[] {new Dictionary<string, object> {["name"] = "tag1", ["meta"] = new Dictionary<string, object> {["priority"] = 1, ["labels"] = new string[] {"x", "y"}}}}}
};
