using System.Collections.Generic;
var Shared = new Dictionary<string, int>[] {
    new Dictionary<string, int> {["value"] = 1}
};
var my_data = new Dictionary<string, int>[][] {
    Shared,
    Shared
};
