using System.Collections.Generic;
using System;
dynamic mgr = new System.Dynamic.ExpandoObject();
mgr.Op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true});
mgr.Op(new Dictionary<string, object> {["type"] = "create", ["pr_id"] = "pr_2"});
