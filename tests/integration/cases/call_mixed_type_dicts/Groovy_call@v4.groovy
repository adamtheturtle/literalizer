class _MgrType { def run(Map _args) { null } }
class _AppType { def mgr = new _MgrType() }
def app = new _AppType()
app.mgr.run(operation: ["type": "create", "pr_id": "pr_1", "draft": true])
app.mgr.run(operation: ["type": "create", "pr_id": "pr_2"])
