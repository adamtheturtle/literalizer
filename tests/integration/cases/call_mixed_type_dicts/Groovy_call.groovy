class _MgrType { def Op(Map _args) { null } }
def mgr = new _MgrType()
mgr.Op(operation: ["type": "create", "pr_id": "pr_1", "draft": true])
mgr.Op(operation: ["type": "create", "pr_id": "pr_2"])
