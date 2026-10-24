interface ICallArg_ {}
fn do_thing(args ...ICallArg_) {}

fn main() {
	do_thing(1);
	do_thing(2);
}
