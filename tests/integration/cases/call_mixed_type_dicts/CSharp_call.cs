using System.Collections.Generic;
using System;
dynamic m = new System.Dynamic.ExpandoObject();
m.Op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true});
m.Op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_2"});
