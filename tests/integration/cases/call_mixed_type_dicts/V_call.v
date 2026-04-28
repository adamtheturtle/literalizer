interface IVal {}
interface ICallArg_ {}
struct MgrType_ {}
fn (r MgrType_) op(args ...ICallArg_) {}
struct AppType_ {
	mgr MgrType_
}

fn main() {
	app := AppType_{}
	app.mgr.op({'type': IVal('create'), 'pr_id': IVal('pr_1'), 'draft': IVal(true)});
	app.mgr.op({'type': IVal('create'), 'pr_id': IVal('pr_2')});
}
