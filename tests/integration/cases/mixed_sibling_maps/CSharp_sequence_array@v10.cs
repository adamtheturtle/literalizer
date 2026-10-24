using System.Collections.Generic;
var my_data = new object?[] {
    new object?[] {new Dictionary<string, object?> {["a"] = 1}, new Dictionary<string, object?> {["a"] = (object?)null}, 42},
    new object?[] {new Dictionary<string, object?> {["a"] = 1}, new Dictionary<string, object?> {["a"] = "s"}, 42},
    new Dictionary<string, object?>[] {new Dictionary<string, object?> {["a"] = 1}, new Dictionary<string, object?> {["a"] = (object?)null}},
    new Dictionary<string, object?>[] {new Dictionary<string, object?> {["a"] = 1}, new Dictionary<string, object?> {["a"] = "s"}}
};
    _ = my_data;
