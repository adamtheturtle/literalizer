using System.Collections.Generic;
using System;
var x = new Dictionary<string, object> {
    ["users"] = (new Dictionary<string, object> {["name"] = "Bob", ["tags"] = ("admin", "user")}, new Dictionary<string, object> {["name"] = "Carol", ["tags"] = ("guest")})
};
