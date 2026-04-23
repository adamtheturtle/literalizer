app = {mgr = {op = function(...) end}}
app.mgr.op({["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true})
app.mgr.op({["type"] = "create", ["pr_id"] = "pr_2"})
