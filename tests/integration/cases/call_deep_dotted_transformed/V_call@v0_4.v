interface ICallArg_ {}
struct ClientType_ {}
fn (r ClientType_) fetch(args ...ICallArg_) ICallArg_ { return 0 }
struct AppType_ {
	client ClientType_
}
fn emit(args ...ICallArg_) {}

fn main() {
	app := AppType_{}
	emit(app.client.fetch('hello'));
	emit(app.client.fetch(42));
	emit(app.client.fetch(true));
}
