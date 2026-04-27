interface IVal {}

fn main() {
	mut my_data := [
		IVal(true),
		IVal('hi'),
		IVal([1, 2]),
		IVal(unsafe { nil }),
	]
	my_data = [
		IVal(true),
		IVal('hi'),
		IVal([1, 2]),
		IVal(unsafe { nil }),
	]
	_ = my_data
}
