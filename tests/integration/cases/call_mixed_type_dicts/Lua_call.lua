app = {mgr = {run = function(...) end}}
app.mgr.run({["type"] = "create", ["pr_id"] = "pr_1", ["draft"] = true})
app.mgr.run({["type"] = "create", ["pr_id"] = "pr_2"})
