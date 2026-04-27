class _mgrType { @discardableResult func op(operation: Any = 0) -> Any { 0 } }
class _appType { var mgr = _mgrType() }
let app = _appType()
app.mgr.op(operation: ["type": "create", "pr_id": "pr_1", "draft": true]);
app.mgr.op(operation: ["type": "create", "pr_id": "pr_2"]);
