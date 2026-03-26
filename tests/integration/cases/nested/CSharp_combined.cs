using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["users"] = (new Dictionary<string, object> {["name"] = "Bob", ["tags"] = ("admin", "user")}, new Dictionary<string, object> {["name"] = "Carol", ["tags"] = ("guest")})
};
my_data = new Dictionary<string, object> {
    ["users"] = (new Dictionary<string, object> {["name"] = "Bob", ["tags"] = ("admin", "user")}, new Dictionary<string, object> {["name"] = "Carol", ["tags"] = ("guest")})
};
