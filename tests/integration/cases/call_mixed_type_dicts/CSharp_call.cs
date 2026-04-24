using System.Collections.Generic;
using System;
class Check {
class MgrType_ { public object op(object operation = null) => null; }
class AppType_ { public MgrType_ mgr = new MgrType_(); }
static AppType_ app = new AppType_();
    public static void Main() {
app.mgr.op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true});
app.mgr.op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_2"});
    }
}
