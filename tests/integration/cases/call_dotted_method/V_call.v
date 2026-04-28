interface IVal {}
interface ICallArg_ {}
struct clientType_ {}
fn (r clientType_) fetch(args ...ICallArg_) {}
struct appType_ {
	client clientType_
}

fn main() {
	app := appType_{}
	app.client.fetch('hello');
	app.client.fetch(42);
	app.client.fetch(true);
}
