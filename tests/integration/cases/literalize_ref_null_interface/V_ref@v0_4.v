interface IVal {}

fn main() {
	value := unsafe { nil }
	my_data := [
		IVal(value),
		IVal(value),
		IVal(unsafe { nil }),
	]
	_ = my_data
}
