interface ICallArg_ {}
struct ClientType_ {}
fn (r ClientType_) fetch(arg0 ICallArg_) {}
struct AppType_ {
	client ClientType_
}

fn main() {
	app := AppType_{}
	app.client.fetch('hello');
	app.client.fetch(42);
	app.client.fetch(true);
}
