interface ICallArg_ {}
struct ThingType_ {}
fn (r ThingType_) first_value(arg0 ICallArg_) {}

fn main() {
	thing := ThingType_{}
	thing.first_value(1);
}
