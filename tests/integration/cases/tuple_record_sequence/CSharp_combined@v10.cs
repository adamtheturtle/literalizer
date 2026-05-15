using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object> {["call"] = "send", ["args"] = (1, "email", "a@gmail.com", 100)},
    new Dictionary<string, object> {["call"] = "recv", ["args"] = (2, "sms", "b@example.com", 200)}
);
my_data = (
    new Dictionary<string, object> {["call"] = "send", ["args"] = (1, "email", "a@gmail.com", 100)},
    new Dictionary<string, object> {["call"] = "recv", ["args"] = (2, "sms", "b@example.com", 200)}
);
