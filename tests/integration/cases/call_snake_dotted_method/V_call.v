interface IVal {}
interface ICallArg_ {}
struct http_clientType_ {}
fn (r http_clientType_) fetch(args ...ICallArg_) {}
struct my_appType_ {
	http_client http_clientType_
}

fn main() {
	my_app := my_appType_{}
	my_app.http_client.fetch('hello');
	my_app.http_client.fetch(42);
	my_app.http_client.fetch(true);
}
