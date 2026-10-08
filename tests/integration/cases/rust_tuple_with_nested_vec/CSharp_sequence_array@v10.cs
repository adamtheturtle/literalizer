using System.Collections.Generic;
var my_data = new Dictionary<string, object> {
    ["lint"] = new object[] {2, new string[] {}},
    ["test"] = new object[] {5, new string[] {"compile"}},
    ["package"] = new object[] {7, new string[] {"link", "test"}}
};
