using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["level1"] = new Dictionary<string, object> {["level2"] = new Dictionary<string, object> {["level3"] = new Dictionary<string, object> {["level4"] = new Dictionary<string, object> {["value"] = "deep", ["items"] = ("a", "b")}}, ["sibling"] = 42}, ["tags"] = (new Dictionary<string, object> {["name"] = "tag1", ["meta"] = new Dictionary<string, object> {["priority"] = 1, ["labels"] = ("x", "y")}})}
};
my_data = new Dictionary<string, object> {
    ["level1"] = new Dictionary<string, object> {["level2"] = new Dictionary<string, object> {["level3"] = new Dictionary<string, object> {["level4"] = new Dictionary<string, object> {["value"] = "deep", ["items"] = ("a", "b")}}, ["sibling"] = 42}, ["tags"] = (new Dictionary<string, object> {["name"] = "tag1", ["meta"] = new Dictionary<string, object> {["priority"] = 1, ["labels"] = ("x", "y")}})}
};
