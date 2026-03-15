using System.Collections.Generic;
var x = new Dictionary<string, object> {
    ["users"] = (new Dictionary<string, object> {["name"] = "Bob", ["tags"] = ("admin", "user")}, new Dictionary<string, object> {["name"] = "Carol", ["tags"] = ("guest")})
};
