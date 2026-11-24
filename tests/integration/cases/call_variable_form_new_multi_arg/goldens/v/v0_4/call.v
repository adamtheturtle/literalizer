interface ICallArg_ {}
fn record_entry(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	my_data := record_entry('a', 1, true)
	_ = my_data
}
