interface ICallArg_ {}
struct ThingType_ {}
fn (r ThingType_) go(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	thing := ThingType_{}
	my_data := thing.go([1])
	_ = my_data
}
