interface IVal {}
interface ICallArg_ {}
struct mgrType_ {}
fn (r mgrType_) op(args ...ICallArg_) {}
struct appType_ {
	mgr mgrType_
}

fn main() {
	app := appType_{}
	app.mgr.op({'type': IVal('create'), 'pr_id': IVal('pr_1'), 'draft': IVal(true)});
	app.mgr.op({'type': IVal('create'), 'pr_id': IVal('pr_2')});
}
