interface IVal {}

fn main() {
	my_data := {
		'a': IVal(1),
		'b': IVal(i64(3000000000)),
		'c': IVal('x'),
	}
	_ = my_data
}
