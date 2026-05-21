interface ICallArg_ {}
fn process(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := process(1, 2)
	_ = my_data
}
