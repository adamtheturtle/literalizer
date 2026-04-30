interface IVal {}

fn main() {
	my_data := [
		IVal(true),
		IVal(1.5),
		IVal(unsafe { nil }),
		IVal("2020-01-01"),
		IVal("2020-01-01T00:00:00+00:00"),
		IVal([]IVal{}),
	]
	_ = my_data
}
