interface ICallArg_ {}
struct ClientType_ {}
fn (r ClientType_) go(arg0 ICallArg_, arg1 ICallArg_) {}
struct AppType_ {
	client ClientType_
}

fn main() {
	app := AppType_{}
	app.client.go([1], [2]);
}
