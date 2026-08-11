using System.Collections.Generic;
using System;
var Foo = new Dictionary<string, string> {
    ["_"] = "_"
};
var my_data = new Dictionary<string, object> {
    ["items"] = (new Dictionary<string, object> {["other"] = 1}, Foo),
    ["mapping"] = new Dictionary<string, object> {["value"] = Foo}
};
