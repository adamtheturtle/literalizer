using System.Collections.Generic;
using System;
class Check {
class WorkerType_ { public object? process(object? values = null, object? count = null) => null; }
class ApiType_ { public WorkerType_ worker = new WorkerType_(); }
static ApiType_ api = new ApiType_();
    public static void Main() {
api.worker.process((1, new Dictionary<string, object?> {}), 42);
api.worker.process((2, new Dictionary<string, string> {["x"] = "s"}), 43);
    }
}
