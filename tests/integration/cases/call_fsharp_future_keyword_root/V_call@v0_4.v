interface ICallArg_ {}
struct ApiType_ {}
fn (r ApiType_) fetch(args ...ICallArg_) {}
struct ProcessType_ {
	api ApiType_
}

fn main() {
	process := ProcessType_{}
	process.api.fetch({'data': 'hello'});
	process.api.fetch({'data': 42});
	process.api.fetch({'data': true});
}
