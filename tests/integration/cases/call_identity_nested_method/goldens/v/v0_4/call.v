interface IVal {}
interface ICallArg_ {}
struct ThingType_ {}
fn (r ThingType_) go() ICallArg_ { return 0 }
struct OuterType_ {
	thing ThingType_
}

fn main() {
	outer := OuterType_{}
	outer.thing.go();
}
