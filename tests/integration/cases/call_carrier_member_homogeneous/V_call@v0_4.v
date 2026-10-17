interface ICallArg_ {}
struct AppType_ {}
fn (r AppType_) go(arg0 ICallArg_, arg1 ICallArg_) {}

fn main() {
	app := AppType_{}
	app.go([1], [2]);
}
