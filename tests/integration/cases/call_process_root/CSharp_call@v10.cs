using System.Collections.Generic;
using System;
class Check {
class ApiType_ { public object? fetch(object? data = null) => null; }
class ProcessType_ { public ApiType_ api = new ApiType_(); }
static ProcessType_ process = new ProcessType_();
    public static void Main() {
process.api.fetch(new Dictionary<string, object?> {["data"] = "hello"});
process.api.fetch(new Dictionary<string, object?> {["data"] = 42});
process.api.fetch(new Dictionary<string, object?> {["data"] = true});
    }
}
