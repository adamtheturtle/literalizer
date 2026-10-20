interface IVal {}
interface ICallArg_ {}
struct ThingType_ {}
fn (r ThingType_) go() ICallArg_ { return 0 }

fn main() {
	thing := ThingType_{}
	thing.go();
}
