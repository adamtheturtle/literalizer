interface IVal {}

fn main() {
	my_data := [
		[[IVal({'\$ref': 'myVar'}), IVal(42), IVal('static')]],
	]
	_ = my_data
}
