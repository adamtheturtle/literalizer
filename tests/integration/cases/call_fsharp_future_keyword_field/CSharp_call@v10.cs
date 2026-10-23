using System.Collections.Generic;
using System;
class Check {
class ProcessType_ { public object? fetch(object? data = null) => null; }
class AppType_ { public ProcessType_ process = new ProcessType_(); }
static AppType_ app = new AppType_();
    public static void Main() {
app.process.fetch(new Dictionary<string, object?> {["data"] = "hello"});
app.process.fetch(new Dictionary<string, object?> {["data"] = 42});
app.process.fetch(new Dictionary<string, object?> {["data"] = true});
    }
}
