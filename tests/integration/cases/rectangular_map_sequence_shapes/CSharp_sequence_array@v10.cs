using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["a"] = new Dictionary<string, int[]>[] {new Dictionary<string, int[]> {["item"] = new int[] {1}}},
    ["b"] = new Dictionary<string, int[]>[] {new Dictionary<string, int[]> {["item"] = new int[] {2}}}
};
    _ = my_data;
