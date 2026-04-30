interface IVal {}

fn main() {
	mut my_data := [
		[{'key': IVal({'\$ref': 'my_var'}), 'count': IVal(42)}],
	]
	my_data = [
		[{'key': IVal({'\$ref': 'my_var'}), 'count': IVal(42)}],
	]
	_ = my_data
}
