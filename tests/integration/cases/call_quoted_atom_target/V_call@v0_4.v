interface ICallArg_ {}
fn DoThing(args ...ICallArg_) {}

fn main() {
	DoThing(1);
	DoThing(2);
}
