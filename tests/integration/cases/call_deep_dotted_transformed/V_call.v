interface IVal {}
interface ICallArg_ {}
struct clientType_ {}
fn (r clientType_) fetch(args ...ICallArg_) ICallArg_ { return 0 }
struct appType_ {
	client clientType_
}
fn emit(args ...ICallArg_) {}

fn main() {
	app := appType_{}
	emit(app.client.fetch('hello'));
	emit(app.client.fetch(42));
	emit(app.client.fetch(true));
}
