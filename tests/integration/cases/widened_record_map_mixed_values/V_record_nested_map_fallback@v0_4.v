interface IVal {}
struct Record0 {
	input map[string]IVal
}

fn main() {
	my_data := [
		Record0{ input: {'a': IVal(1)} },
		Record0{ input: {'b': IVal('two')} },
	]
	_ = my_data
}
