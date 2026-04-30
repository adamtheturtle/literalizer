using System.Collections.Generic;
using System;
class Check {
class MgrType_ { public object run(object operation = null) => null; }
class AppType_ { public MgrType_ mgr = new MgrType_(); }
static AppType_ app = new AppType_();
    public static void Main() {
app.mgr.run(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true});
app.mgr.run(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_2"});
    }
}
