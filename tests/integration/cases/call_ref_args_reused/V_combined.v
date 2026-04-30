interface IVal {}

fn main() {
	mut my_data := [
		[IVal({'\$ref': 'repeated_var'}), IVal(1)],
		[IVal({'\$ref': 'single_var'}), IVal(0)],
		[IVal({'\$ref': 'repeated_var'}), IVal(8)],
	]
	my_data = [
		[IVal({'\$ref': 'repeated_var'}), IVal(1)],
		[IVal({'\$ref': 'single_var'}), IVal(0)],
		[IVal({'\$ref': 'repeated_var'}), IVal(8)],
	]
	_ = my_data
}
