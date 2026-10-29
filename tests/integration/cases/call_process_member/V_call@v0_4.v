interface ICallArg_ {}
struct ProcessType_ {}
fn (r ProcessType_) fetch(arg0 ICallArg_) {}
struct AppType_ {
	process ProcessType_
}

fn main() {
	app := AppType_{}
	app.process.fetch({'data': 'hello'});
	app.process.fetch({'data': 42});
	app.process.fetch({'data': true});
}
