interface IVal {}
interface ICallArg_ {}
struct ClientType_ {}
fn (r ClientType_) fetch(args ...ICallArg_) {}
struct AppType_ {
	client ClientType_
}

fn main() {
	app := AppType_{}
	app.client.fetch('hello');
	app.client.fetch(42);
	app.client.fetch(true);
}
