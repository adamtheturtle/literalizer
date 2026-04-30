interface IVal {}

fn main() {
	mut my_data := [
		[[IVal({'\$ref': 'myVar'}), IVal(42), IVal('static')]],
	]
	my_data = [
		[[IVal({'\$ref': 'myVar'}), IVal(42), IVal('static')]],
	]
	_ = my_data
}
