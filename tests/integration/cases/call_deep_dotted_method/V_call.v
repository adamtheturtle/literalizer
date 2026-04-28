interface IVal {}
interface ICallArg_ {}
struct clientType_ {}
fn (r clientType_) post(args ...ICallArg_) {}
struct apiType_ {
	client clientType_
}
struct objType_ {
	api apiType_
}

fn main() {
	obj := objType_{}
	obj.api.client.post('hello');
	obj.api.client.post(42);
	obj.api.client.post(true);
}
