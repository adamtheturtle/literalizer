using System.Collections.Generic;
var my_data = new Dictionary<string, object> {
    ["metrics"] = new Dictionary<string, int> {["count"] = 100, ["rate"] = 50},
    ["flags"] = new Dictionary<string, int> {["retries"] = 3, ["timeout"] = 30}
};
