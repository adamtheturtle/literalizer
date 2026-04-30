interface IVal {}

fn main() {
	mut my_data := [
		[[IVal({'\$ref': 'my_var'}), IVal(42), IVal('static')]],
		[[IVal({'\$ref': 'my_other'}), IVal(7), IVal('label')]],
	]
	my_data = [
		[[IVal({'\$ref': 'my_var'}), IVal(42), IVal('static')]],
		[[IVal({'\$ref': 'my_other'}), IVal(7), IVal('label')]],
	]
	_ = my_data
}
