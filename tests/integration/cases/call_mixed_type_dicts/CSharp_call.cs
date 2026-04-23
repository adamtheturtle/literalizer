using System.Collections.Generic;
using System;
dynamic app = new System.Dynamic.ExpandoObject();
app.mgr.op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true});
app.mgr.op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_2"});
