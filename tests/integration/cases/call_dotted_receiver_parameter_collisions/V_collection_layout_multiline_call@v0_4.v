interface IVal {}
interface ICallArg_ {}
struct WorkerType_ {}
fn (r WorkerType_) process(arg0 ICallArg_, arg1 ICallArg_) {}
struct ApiType_ {
	worker WorkerType_
}

fn main() {
	api := ApiType_{}
	api.worker.process(map[string]IVal{}, map[string]IVal{});
}
