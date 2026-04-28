interface IVal {}

fn main() {
	mut my_data := [
		IVal({'a': 1}),
		IVal('hello'),
	]
	my_data = [
		IVal({'a': 1}),
		IVal('hello'),
	]
	_ = my_data
}
