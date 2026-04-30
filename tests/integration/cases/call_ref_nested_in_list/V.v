interface IVal {}

fn main() {
	my_data := [
		[[IVal({'\$ref': 'my_var'}), IVal(42), IVal('static')]],
		[[IVal({'\$ref': 'my_other'}), IVal(7), IVal('label')]],
	]
	_ = my_data
}
