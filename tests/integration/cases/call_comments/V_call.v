interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	// Test cases
	process('hello');  // single word
	process('hello world');  // two words
	// trailing comment
}
