interface IVal {}
interface ICallArg_ {}
struct ThingType_ {}
fn (r ThingType_) go(arg0 ICallArg_) ICallArg_ { return 0 }

fn main() {
	thing := ThingType_{}
	my_data := thing.go([]IVal{})
	_ = my_data
}
