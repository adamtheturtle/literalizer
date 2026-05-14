interface ICallArg_ {}
struct ClientType_ {}
fn (r ClientType_) post(args ...ICallArg_) {}
struct ApiType_ {
	client ClientType_
}
struct ObjType_ {
	api ApiType_
}

fn main() {
	obj := ObjType_{}
	obj.api.client.post('hello');
	obj.api.client.post(42);
	obj.api.client.post(true);
}
