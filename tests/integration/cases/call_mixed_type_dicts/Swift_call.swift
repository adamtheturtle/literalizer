class _mgrType { func Op(operation: Any = 0) -> Any { 0 } }
let mgr = _mgrType()
mgr.Op(operation: ["type": "create", "pr_id": "pr_1", "draft": true]);
mgr.Op(operation: ["type": "create", "pr_id": "pr_2"]);
