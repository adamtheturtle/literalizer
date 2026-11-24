interface IVal {}
struct Record0 {
	input map[string]IVal
}

fn main() {
	my_data := [
		Record0{ input: {'a': IVal(unsafe { nil })} },
		Record0{ input: {'b': IVal(unsafe { nil })} },
	]
	_ = my_data
}
