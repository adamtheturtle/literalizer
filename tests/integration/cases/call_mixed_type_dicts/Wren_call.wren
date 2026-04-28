class AppMgr_ {
    construct new() {}
    op(operation) {}
}
class App_ {
    mgr { _mgr }
    construct new() {
        _mgr = AppMgr_.new()
    }
}
var app = App_.new()
app.mgr.op({"type": "create", "pr_id": "pr_1", "draft": true})
app.mgr.op({"type": "create", "pr_id": "pr_2"})
