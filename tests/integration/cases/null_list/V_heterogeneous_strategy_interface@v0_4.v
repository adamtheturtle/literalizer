interface IVal {}

fn main() {
	my_data := [
		IVal(unsafe { nil }),
		IVal(unsafe { nil }),
	]
	_ = my_data
}
