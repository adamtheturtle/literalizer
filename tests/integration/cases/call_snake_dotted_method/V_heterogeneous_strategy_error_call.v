interface ICallArg_ {}
struct Http_clientType_ {}
fn (r Http_clientType_) fetch(args ...ICallArg_) {}
struct My_appType_ {
	http_client Http_clientType_
}

fn main() {
	my_app := My_appType_{}
	my_app.http_client.fetch('hello');
	my_app.http_client.fetch(42);
	my_app.http_client.fetch(true);
}
