interface IVal {}
interface ICallArg_ {}
struct ApiType_ {}
fn (r ApiType_) process(arg0 ICallArg_) {}

fn main() {
	api := ApiType_{}
	api.process(map[string]IVal{});
}
