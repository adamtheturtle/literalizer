using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["positive"] = new Dictionary<string, long[]>[] {new Dictionary<string, long[]> {["item"] = new long[] {2147483648}}},
    ["negative"] = new Dictionary<string, long[]>[] {new Dictionary<string, long[]> {["item"] = new long[] {-2147483649}}},
    ["mixed"] = new Dictionary<string, long[]>[] {new Dictionary<string, long[]> {["item"] = new long[] {0, 2147483648}}}
};
    _ = my_data;
